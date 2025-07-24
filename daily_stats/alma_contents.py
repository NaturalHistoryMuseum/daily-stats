import datetime
import urllib.parse

import pandas as pd
import xmltodict

from daily_stats.config import Config
from daily_stats.db import AlmaCsfPackageComp, get_sessionmaker
from daily_stats.logger import get_logger
from daily_stats.utils import make_request


def get_alma_contents(config: Config):
    """
    Retrieve data from the ExLibris Alma API, summarise, and insert it into the stats
    database.
    """
    logger = get_logger(config, 'alma_contents', 'alma_contents.log')
    sessionmaker = get_sessionmaker(config)

    url = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/analytics/reports'
    params = {
        'path': '/shared/Natural History Museum UK (NHM)/Reports/JTD/ItemCount',
        'limit': 1000,
        'apikey': config.alma_token,
    }

    # Query API and flatten result
    r = make_request(url, params=urllib.parse.urlencode(params, safe='/'))
    doc = xmltodict.parse(r.text)

    # Navigate past all the headers etc to get to the row-level data
    row_data = doc['report']['QueryResult']['ResultXml']['rowset']['Row']
    mapped_row_data = [_translate_library(b) for b in row_data]

    # Today's date
    harvest_date = datetime.date.today()

    # Get summary for each type of collection/bib level combo (was 600 rows per day
    # otherwise and unnecessary)
    df = (
        pd.DataFrame.from_records(
            [
                {
                    'bib_level': row['Column1'],
                    'collection': row['library_code'],
                    'date': harvest_date,
                    'record_count': int(row['Column3']),
                }
                for row in mapped_row_data
            ]
        )
        .groupby(['bib_level', 'collection', 'date'])
        .sum()
        .reset_index()
    )

    with sessionmaker.begin() as session:
        records = [AlmaCsfPackageComp(**r) for r in df.to_dict(orient='records')]
        session.add_all(records)

    logger.info(f'Added {len(df)} records.')


def _translate_library(row):
    """
    Map library names to special/modern collections.
    """
    if row['Column2'] == 'PAL-ARTHRO':
        row['library_code'] = 'modern-collections'
    elif 'MSS' in row['Column2'] or 'SC' in row['Column2'] or 'ART' in row['Column2']:
        row['library_code'] = 'special-collections'
    elif row['Column2'] in ['BOT-HENREY', 'BOT-CRYPSC', 'GEN-OWEN', 'TRI-ROTHSC']:
        row['library_code'] = 'special-collections'
    else:
        row['library_code'] = 'modern-collections'
    return row


if __name__ == '__main__':
    conf = Config()
    get_alma_contents(conf)
