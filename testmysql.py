import MySQLdb as msql

conn = msql.connect("localhost", "root", "admin")

if (conn):
    print "Connection Successful"
a = conn.cursor()
query = str("show global status like '%writ%'")
a.execute(query)
result = a.fetchall()
for i in result:
    if i[0] == 'Innodb_log_writes':
        log_writes = int(i[1])
    elif i[0] == 'Innodb_dblwr_writes':
        dblwr_writes = int(i[1])
    elif i[0] == 'Innodb_pages_written':
        pages_written = int(i[1])
    if i[0] == 'Innodb_data_writes':
        data_writes = int(i[1])

print "total writes  = ", log_writes + dblwr_writes + pages_written + data_writes



conn.close()




# Show global status like '%write%' gives the following variables
#
# mysql> show global status like '%write%';
#
# +-----------------------------------+-------+
# | Variable_name                     | Value |
# +-----------------------------------+-------+
# | Delayed_writes                    | 0     |
# | Handler_write                     | 271   |
# | Innodb_buffer_pool_write_requests | 515   |
# | Innodb_data_pending_writes        | 0     |
# | Innodb_data_writes                | 56    |
# | Innodb_dblwr_writes               | 1     |
# | Innodb_log_write_requests         | 0     |
# | Innodb_log_writes                 | 2     |
# | Innodb_os_log_pending_writes      | 0     |
# | Innodb_truncated_status_writes    | 0     |
# | Key_write_requests                | 0     |
# | Key_writes                        | 0     |
# +-----------------------------------+-------+
# 12 rows in set (0.00 sec)
#
# as there was no defined parameter to find the total number of disk writes by MySQL, I assumed that it
# should be the total sum of all the write variables

# Innodb_data_writes - The total number of data writes
#
# Innodb_dblwr_writes - The number of doublewrite operations that have been performed.
#
# Innodb_log_writes - The number of physical writes to the log file
#
# Key_writes - The number of physical writes of a key block to disk
