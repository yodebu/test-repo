#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import sys

import MySQLdb as msql  # to use the MySQL Python Connector provided by MySQL

# Database Credentials

host = 'localhost'
user = 'root'
password = 'admin'
database = 'test'

try:
    con = msql.connect(host, user, password)
    cur = con.cursor()

    #		mysql> select * from information_schema.engines;
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
    # the value returned to res will be a YES/NO/DEFAULT
    # DEFAULT means the plugin InnoDB is the default storage engine and enabled by default
    if res == 'YES' or res == 'DEFAULT':
        print "InnoDB Plugin is Enabled"
    elif res == 'NO':
        print "InnoDB Module is not enabled"
    else:
        print "InnoDB Module is not installed"

except msql.Error, e:
    # catches Error/Warnings on the MySQL command executions and logs them to the screen
    # i.e. prints them to display
    # and exits the program

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    # closing the connection after the work is done

    if con:
        con.close()
