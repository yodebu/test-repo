import MySQLdb as msql

conn = msql.connect("localhost", "root", "admin")

if (conn):
    print "Connection Successful"
a = conn.cursor()
query = str("show global status like '%writ%'")
a.execute(query)
result = a.fetchall()
print result
