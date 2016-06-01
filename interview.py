import MySQLdb as msql


def connect_mysql(hostname, user, password):
    '''

    :param hostname: IP ADDRESS
    :param user: username
    :param password:
    :return:
    '''
    conn = msql.connect(hostname, user, password)
    return conn


def check_innodb(conn):
    cur = conn.cursor()



    return
