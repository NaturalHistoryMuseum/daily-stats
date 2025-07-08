import pymysql


def query_db(sql):
    """
    Read and write from mySQL database
    :param sql: String script to run
    :return: Cursor
    """
    args = get_keys('msq-permissions.txt')
    if len(args) == 4:
        # old style permissions format with host, user, password, db
        db = pymysql.connect(host=args[0], user=args[1], password=args[2], db=args[3])
    elif len(args) == 8:
        # new style permissions with addition of port and ssl config
        db = pymysql.connect(
            host=args[0],
            port=int(args[1]),
            user=args[2],
            password=args[3],
            db=args[4],
            ssl_ca=args[5],
            ssl_key=args[6],
            ssl_cert=args[7],
        )
    else:
        print('Permissions file must have 5 or 7 args specified')
        exit(1)

    with db:
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            return cursor
        except pymysql.Error as e:
            print(sql)
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


def update_db(sql, row_data):
    """
    Batch write to mySQL database
    :param sql: String script
    :param row_data: List of parameters to be used with the query
    :return: Cursor
    """
    host, user, password, database = get_keys('msq-permissions.txt')
    with pymysql.connect(host=host, user=user, password=password, database=database) as db:
        cursor = db.cursor()
        try:
            cursor.executemany(sql, row_data)
            db.commit()
            return cursor
        except pymysql.Error as e:
            print(e)
