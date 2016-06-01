import MySQLdb as msql

conn = msql.connect("localhost", "root", "admin")

if (conn):
    print "Connection Succesfull"
a = conn.cursor()
print a
