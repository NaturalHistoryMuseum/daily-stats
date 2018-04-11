import pymysql


def query_db(sql):
    """
    Read and write from mySQL database
    :param sql: String script to run
    :return: Cursor
    """
    host, user, password, database = get_keys('server-permissions.txt')
    with pymysql.connect(host=host, user=user, password=password, db=database) as cursor:
        try:
            cursor.execute(sql)
            return cursor
        except pymysql.Error as e:
            print(e)


def get_keys(filename):
    """
    Reads auth details from file
    :param filename: String filename
    :return: List<String> of auth details
    """
    with open(filename, 'r') as f:
        keys = f.read().splitlines()
        return keys
