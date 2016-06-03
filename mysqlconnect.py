#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import ConfigParser
import sys

import MySQLdb as msql

conn = False


# GLobal variable to hold the connection handle

def db_connect(connectstring):
    '''
    Returns a database connection/handle given the connectstring
    This function saves the database connection, so if you
    invoke this again, it gives you the same one, rather
    than making a second connection.
    Singleton pattern.
    this fucntion returns the cursor of the connection
    '''

    global conn
    if not conn:
        try:
            conn = msql.connect(**connectstring)
            # so modifications take effect automatically
            conn.autocommit(True)
        except msql.Error, e:
            print ("Couldn't connect to database. MySQL error %d: %s" %
                   (e.args[0], e.args[1]))
            sys.exit(3)
    return conn.cursor()



def config_read_file(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser.ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    print db
    return db


def check_innodb(cur):
    #	mysql> select * from information_schema.engines;
    #	+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
    #	| ENGINE             | SUPPORT | COMMENT                                                        | TRANSACTIONS | XA   | SAVEPOINTS |
    #	+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
    #	| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
    #	| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
    #	| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
    #	| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
    #	| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
    #	| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
    #	| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
    #	| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
    #	| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
    #	+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
    #	9 rows in set (0.00 sec)

    # hence we limit the Query to only the SUPPORT column where ENGINE = InnoDB
    # output can be = DEFAULT, YES, NO or the Query can return NULL/EMPTY SET or 0 rows
    # if the Engine InnoDB is not installed

    sqlstring = "SELECT SUPPORT FROM INFORMATION_SCHEMA.ENGINES WHERE ENGINE = 'InnoDB';"
    cur.execute(sqlstring)

    # used fetchone() than fetchall() because the SQL query will by default return one row
    res = cur.fetchone()
    # converted tuple to string
    res = str(res[0])
    return res


def find_total_write(cursor):
    '''

    :param cursor: MySQLdb Cursor() object
    :return: total writes of disk
    '''

    # PERFORMANCE SCHEMA = mysql dev forums
    # The Performance Schema monitors server events.
    # An “event” is anything the server does that takes time
    # and has been instrumented so that timing information can be collected.
    #
    # In general, an event could be a function call, a wait for the operating system,
    # a stage of an SQL statement execution such as parsing or sorting, or an entire statement or group of statements.
    # Event collection provides access to information about synchronization calls
    # (such as for mutexes) and file I/O calls for the server and for several storage engines.

    # File I/O Summaries:
    #
    #  file_summary_by_event_name: File events summarized per event name
    #  file_summary_by_instance: File events summarized per file instance


    # using two queries which calculate the total mySAM write operations and the InnoDB write operations


    #
    # mysql > select sum(count_write) from file_summary_by_instance where file_summary_by_instance.event_name like '%myISAM%';
    # +------------------+
    # | sum(count_write) |
    # +------------------+
    # | 0                |
    # +------------------+
    # 1 row in set(0.00 sec)
    #
    # Counts the total number of writes by the InnoDB
    #
    query = str(
        "select cast(sum(count_write) as unsigned) from file_summary_by_instance where file_summary_by_instance.event_name like '%myISAM%';")
    cursor.execute(query)
    result_isam = cursor.fetchone()
    result_isam = int(result_isam[0])  # isam_write count
    # print result_isam

    # mysql > select sum(count_write) from file_summary_by_instance where file_summary_by_instance.event_name like '%InnoDB%';
    # +------------------+
    # | sum(count_write) |
    # +------------------+
    # | 56               |
    # +------------------+
    # 1 row in set(0.00 sec)
    #
    # Counts the total number of writes by the InnoDB
    #
    query2 = str(
        "select cast(sum(count_write) as unsigned) from file_summary_by_instance where file_summary_by_instance.event_name like '%InnoDB%';")
    cursor.execute(query2)
    result_innodb = cursor.fetchone()
    result_innodb = int(result_innodb[0])  # innodb_write count
    # print result_innodb
    total = result_isam + result_innodb
    print "total writes  = " + str(total)
    return total



def main():
    '''
    this is the main function of the program

    :return:
    '''

    # # read the config.ini for the credentials
    #
    # we directly provide the db = performance_schema because
    # we are reading variables from the performance_schema database

    filename = 'config.ini'
    section = 'mysql'

    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored

    if len(sys.argv) is 2:
        filename = sys.argv[1]
    if len(sys.argv) is 3:
        section = sys.argv[2]
    # you may need not provide the system arguments and can directly use the included config.ini file which
    # is included by default

    credentials = config_read_file(filename, section)

    try:

        cur = db_connect(credentials)
        res = check_innodb(cur)
        # the value returned to res will be a YES/NO/DEFAULT
        # DEFAULT means the plugin InnoDB is the default storage engine and enabled by default
        if res == 'YES' or res == 'DEFAULT':
            print "InnoDB Plugin is Enabled"
            c = find_total_write(cur)
        elif res == 'NO':
            print "InnoDB Module is not enabled"
        else:
            print "InnoDB Module is not installed"

    except msql.Error, e:
        # catches Error/Warnings on the MySQL command executions and logs them to the screen
        # i.e. prints them to display
        # and exits the program returning 1

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        # closing the connection after the work is done

        if conn:
            conn.close()


if __name__ == '__main__':
    main()

