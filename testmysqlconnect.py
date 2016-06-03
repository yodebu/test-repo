#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import mysqlconnect as ms


def test_suite():
    test_suit = [({'passwd': 'admin', 'host': 'localhost', 'db': 'performance_schema', 'user': 'root'}, 'PASS'),
                 ({'passwd': 'exam', 'host': 'localhost', 'db': 'performance_schema', 'user': 'root'}, 'FAIL')]
    for connstring, ret in test_suit:
        if ms.db_connect(connstring):
            print "PASS"
        else:
            print "FAIL"


test_suite()

# will give the correct answer for the first time and then wrong answer from next times because of singleton connection
#
# 1st run output =
#
# PASS
# FAIL
#
#
# 2nd and consecutive runs output =
#
# PASS
# PASS

# this test checks the singleton connection as well as because it does not create a new connection
# when a connect statement is evoked
