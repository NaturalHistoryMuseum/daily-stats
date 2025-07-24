import itertools
from datetime import datetime as dt

import sqlalchemy as sa
from requests import HTTPError

from daily_stats.config import Config
from daily_stats.db import GBIFBibliometrics, GBIFCitation, get_sessionmaker
from daily_stats.logger import get_logger
from daily_stats.utils import make_request


def get_gbif_citations(config: Config):
    logger = get_logger(config, 'gbif_citations')
    sessionmaker = get_sessionmaker(config)

    # get list of works that cited NHM specimens
    works = []
    url = 'https://api.gbif.org/v1/literature/search'
    params = {'gbifDataSetKey': '7e380070-f762-11e1-a439-00145eb45e9a', 'limit': 100}
    try:
        for offset in itertools.count(step=100):
            params['offset'] = offset
            r = make_request(url, params=params)
            r.raise_for_status()
            results = r.json()['results']

            # only keep results with an id
            works.extend([result for result in results if 'id' in result])

            if r.json()['endOfRecords']:
                break
    except HTTPError as e:
        logger.error(e)

    logger.info(f'Found {len(works)} works')

    separator = '; '
    all_citations = {}

    # flatten API result and add defaults
    for c in works:
        citation_dict = {
            # table fields
            'id': c['id'],
            'abstract': c.get('abstract', '').replace('\n', ''),
            'authors': '; '.join([' '.join(n.values()) for n in c.get('authors', [])]),
            'countries_of_researcher': separator.join(
                c.get('countriesOfResearcher', [])
            ),
            'doi': c.get('identifiers', {}).get('doi'),
            'harvest_date': dt.strptime(
                c.get('discovered', '1111-01-01'), '%Y-%m-%d'
            ).date(),
            'language': c.get('language'),
            'literature_type': c.get('literatureType'),
            'month': c.get('month', 0),
            'nhm_record_count': None,
            'open_access': c.get('openAccess'),
            'peer_review': c.get('peerReview'),
            'pub_date': dt.strptime(
                c.get('published', '1111-01-01')[:10], '%Y-%m-%d'
            ).date(),
            'publisher': c.get('publisher', '').replace('\n', ''),
            'source': c.get('source', '').replace('\n', ''),
            'title': c.get('title', '').replace('\n', ''),
            'topics': separator.join(c.get('topics', [])),
            'total_dataset_count': None,
            'total_record_count': None,
            'update_date': dt.strptime(c['modified'][0:10], '%Y-%m-%d').date(),
            'year': c.get('year'),
            # other
            'gbif_dk_list': c.get('gbifDownloadKey'),
        }

        # make these null if they're falsy (e.g. empty strings or 0)
        for k in [
            'abstract',
            'authors',
            'countries_of_researcher',
            'publisher',
            'source',
            'title',
            'topics',
        ]:
            if not citation_dict[k]:
                citation_dict[k] = None

        all_citations[c['id']] = citation_dict

    # identify citations to be removed, added and updated on database
    api_citation_ids = set(all_citations.keys())
    with sessionmaker.begin() as session:
        select_stmt = sa.select(GBIFCitation.id, GBIFCitation.update_date).order_by(
            GBIFCitation.id
        )
        database_citations = session.execute(select_stmt).all()
    database_citation_ids = set([c[0] for c in database_citations])
    logger.info(f'Found {len(database_citation_ids)} existing citations')
    # anything in the db but not the API needs deleting from the db
    citation_ids_to_delete = list(database_citation_ids - api_citation_ids)
    logger.info(f'{len(citation_ids_to_delete)} citations to delete')
    # anything in the api and not the db needs adding to the db
    citation_ids_to_add = list(api_citation_ids - database_citation_ids)
    logger.info(f'{len(citation_ids_to_add)} citations to add')
    # anything in both needs to be checked for latest update
    common_citation_ids = database_citation_ids & api_citation_ids
    common_citations = filter(lambda x: x in common_citation_ids, database_citations)

    # identify updated records since last run and queue for deletion and re-insertion
    for citation_id, last_updated in common_citations:
        api_record = all_citations[citation_id]

        # if api result update > database update date, append to 'add' list
        # any duplicate keys will trigger an update
        if api_record['update_date'] > last_updated:
            citation_ids_to_add.append(citation_id)

    # remove outdated citations
    if citation_ids_to_delete:
        with sessionmaker.begin() as session:
            delete_stmt = sa.delete(GBIFCitation).where(
                GBIFCitation.id.in_(citation_ids_to_delete)
            )
            delete_result = session.execute(delete_stmt)
            logger.info(f'Deleted {delete_result.rowcount} citations')

            # check for and remove any orphan rows in the biblio table
            # the NOT NULL is _required_ otherwise this will return nothing
            orphan_delete_stmt = sa.delete(GBIFBibliometrics).where(
                GBIFBibliometrics.doi.notin_(
                    sa.select(GBIFCitation.doi)
                    .distinct()
                    .where(GBIFCitation.doi.isnot(None))
                )
            )
            orphan_delete_result = session.execute(orphan_delete_stmt)
            logger.info(
                f'Deleted {orphan_delete_result.rowcount} orphaned biblio records'
            )

    # add new + updated citations
    if citation_ids_to_add:
        new_citation_records = []
        total_citations_to_add = len(citation_ids_to_add)
        for ix, cid in enumerate(citation_ids_to_add):
            citation_dict = all_citations[cid]
            if citation_dict['gbif_dk_list']:
                citation_dict = _aggregate_download_stats(citation_dict, logger)
            new_citation_records.append(GBIFCitation.strip(citation_dict))
            logger.info(
                f'Adding {ix + 1}/{total_citations_to_add}: {citation_dict["title"]}'
            )

        with sessionmaker.begin() as session:
            session.execute(sa.insert(GBIFCitation), new_citation_records)


def _aggregate_download_stats(citation_record, logger):
    """
    Retrieve and reshape download data from GBIF API.

    Uses download keys to retrieve download counts + source dataset keys for each
    download cited in the paper.

    :param citation_record: citation dict to be updated and returned
    """
    # may be multiple download keys
    gbif_download_keys = citation_record['gbif_dk_list']

    # aggregate and de-duplicate dataset references and record counts over all downloads
    # for this citation
    total_citation_record_count = 0
    all_citation_datasets = set()
    total_nhm_record_count = 0

    # for each gbif download key, get the component dataset keys and record counts
    for k in gbif_download_keys:
        # base url is the same for both requests
        download_stats_url = f'http://api.gbif.org/v1/occurrence/download/{k}'

        # get overall record count for this download record
        r = make_request(download_stats_url)
        try:
            r.raise_for_status()
            total_citation_record_count += r.json().get('totalRecords', 0)
        except Exception as e:
            # catch everything to stop the whole thing crashing if one request fails
            logger.error(e)

        # get datasets included in the download and number of NHM records, if any
        datasets = set()
        nhm_record_count = 0
        download_datasets_url = download_stats_url + '/datasets'
        params = {'limit': 500}
        for offset in itertools.count(step=500):
            params['offset'] = offset
            try:
                r = make_request(download_datasets_url, params=params)
                r.raise_for_status()
                dataset_results = r.json()

                for d in dataset_results['results']:
                    dataset_key = d['datasetKey']
                    datasets.add(dataset_key)
                    if dataset_key == '7e380070-f762-11e1-a439-00145eb45e9a':
                        nhm_record_count += d['numberRecords']

                if (
                    dataset_results['endOfRecords']
                    or len(dataset_results['results']) == 0
                ):
                    break
            except Exception as e:
                # catch everything to stop the whole thing crashing if one request fails
                logger.error(e)

        # add to the current set of dataset IDs
        all_citation_datasets |= datasets
        # increment NHM count
        total_nhm_record_count += nhm_record_count

    # update the citation record with total count of nhm records, total records cited
    # and dataset count
    citation_record['nhm_record_count'] = total_nhm_record_count
    citation_record['total_record_count'] = total_citation_record_count
    citation_record['total_dataset_count'] = len(all_citation_datasets)

    return citation_record


if __name__ == '__main__':
    conf = Config()
    get_gbif_citations(conf)
