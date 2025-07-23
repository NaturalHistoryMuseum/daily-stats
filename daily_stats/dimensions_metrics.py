import datetime
import time

from requests import HTTPError
from sqlalchemy import distinct, func, select

from daily_stats.config import Config
from daily_stats.db import GBIFBibliometrics, GBIFCitation, get_session
from daily_stats.logger import get_logger
from daily_stats.utils import make_request


def get_dimensions_metrics(config: Config):
    """
    Get citations metrics from the dimensions API.
    """
    logger = get_logger(config, 'dimensions_metrics', 'dimensions_metrics.log')

    # Today's date
    harvest_date = datetime.date.today()

    records = []

    count_stmt = select(func.count(distinct(GBIFCitation.doi))).where(
        GBIFCitation.doi.isnot(None)
    )
    select_stmt = (
        select(GBIFCitation.doi).distinct().where(GBIFCitation.doi.isnot(None))
    )
    session = get_session(config)
    with session:
        total = session.execute(count_stmt).all()[0][0]
        dois = session.scalars(select_stmt)

    # For all DOIs, get citation count
    for ix, doi in enumerate(dois):
        url = f'https://metrics-api.dimensions.ai/doi/{doi}'
        logger.info(f'[{ix + 1}/{total}] {url}')
        try:
            r = make_request(url)
            r.raise_for_status()
            records.append(
                GBIFBibliometrics(
                    doi=doi,
                    times_cited=r.json()['times_cited'] or 0,
                    field_citation_ratio=r.json()['field_citation_ratio'] or 0,
                    relative_citation_ratio=r.json()['relative_citation_ratio'] or 0,
                    harvest_date=harvest_date,
                )
            )
        # Skip over DOIs which aren't found
        except HTTPError:
            pass
        # Throttle query rate to comply with API terms of use
        time.sleep(1)

    with session:
        session.add_all(records)
        session.commit()


if __name__ == '__main__':
    conf = Config()
    get_dimensions_metrics(conf)
