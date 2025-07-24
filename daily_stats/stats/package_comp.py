import itertools
from datetime import date

import sqlalchemy as sa
from requests import HTTPError

from daily_stats.config import Config
from daily_stats.db import PackageComp, get_sessionmaker
from daily_stats.logger import get_logger
from daily_stats.utils import make_request


def get_package_comp(config):
    logger = get_logger(config, 'package_comp')
    sessionmaker = get_sessionmaker(config)

    try:
        url = 'https://data.nhm.ac.uk/api/3/action/dataset_statistics'
        r = make_request(url)
        r.raise_for_status()
        resources = r.json()['result']['resources']
    except HTTPError as e:
        logger.error(e.response)
        resources = []

    collections = ['collection specimens', 'index lot collection', 'artefacts']
    harvest_date = date.today()

    def _summarise_pkg(package_name, resource_list):
        # make it into a list because we need to access the items multiple times
        resource_list = list(resource_list)
        # should be the same for all items, so just use the first one
        pkg_title = (
            resource_list[0]['pkg_title'].replace("'", "''").replace('\u2013', '')
        )
        pkg_type = (
            'collection records'
            if pkg_title.lower() in collections
            else 'research records'
        )
        return {
            'date': harvest_date,
            'pkg_name': package_name.replace("'", "''"),
            'pkg_title': pkg_title,
            'pkg_type': pkg_type,
            'record_count': sum([res['total'] for res in resource_list]),
        }

    # group the resources by package and summarise
    packages = [
        _summarise_pkg(pkg_name, res_list)
        for pkg_name, res_list in itertools.groupby(
            sorted(resources, key=lambda x: x['pkg_name']), key=lambda x: x['pkg_name']
        )
    ]

    # if there are no records, trying to bulk insert will add a null record
    if not packages:
        logger.info('No records to add; exiting.')
        return

    with sessionmaker.begin() as session:
        session.execute(sa.insert(PackageComp), packages)

    logger.info(f'Added {len(packages)} records.')


if __name__ == '__main__':
    conf = Config()
    get_package_comp(conf)
