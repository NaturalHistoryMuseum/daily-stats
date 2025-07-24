from datetime import date

from requests import HTTPError

from daily_stats.config import Config
from daily_stats.db import SpecimenImages, get_sessionmaker
from daily_stats.logger import get_logger
from daily_stats.utils import make_request


def get_portal_images(config):
    logger = get_logger(config, 'portal_images')
    sessionmaker = get_sessionmaker(config)

    resource_id = '05ff2255-c38a-40c9-b657-4ccb55ab2feb'

    try:
        url = 'https://data.nhm.ac.uk/api/3/action/vds_multi_stats'
        params = {'resource_ids': resource_id, 'field': 'associatedMediaCount'}
        r = make_request(url, params=params)
        result = r.json()['result']
    except HTTPError as e:
        logger.error(e.response)
        return

    with sessionmaker.begin() as session:
        session.add(
            SpecimenImages(
                date=date.today(),
                image_count=int(result['sum']),
                imaged_specimens=int(result['count']),
                resource_id=resource_id,
            )
        )

    logger.info('Added portal image summary.')


if __name__ == '__main__':
    conf = Config()
    get_portal_images(conf)
