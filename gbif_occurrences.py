import requests
import pymysql
import datetime


def get_keys():
    # Get gbif download keys from citations table
    with open('local_details.txt', 'r') as f:
        keys = f.read().splitlines()
        host, user, password, database = keys

    # Connect to database:
    with pymysql.connect(host=host, user=user, password=password, db=database) as cursor:
        sql = f"SELECT id, gbif_download_key FROM gbif_citations;"

        try:
            cursor.execute(sql)
            occurrences = {}
            for n in cursor.fetchall():
                downloads = {}
                gk_list = n[1].split("; ")
                # For each gkey list, split apart and add to dict with corresponding id
                for gk in gk_list:
                    downloads['gbif_download_key'] = gk
                    downloads['gid'] = n[0]
                    # Add to occurrences dict
                    occurrences[gk] = downloads

        except pymysql.Error as e:
            print(sql)
            print(e)


if __name__ == '__main__':
    get_keys()
