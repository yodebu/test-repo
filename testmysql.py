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




# Show global status like '%write%' gives the following variables
#
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
# should be the total sum of all the write variables -
#
#
# this is what I got after a detailed study of the status variables -

# Innodb_data_writes - The total number of data writes
#
# Innodb_dblwr_writes - The number of doublewrite operations that have been performed.
#
# Innodb_log_writes - The number of physical writes to the log file
#
# Key_writes - The number of physical writes of a key block to disk


# * Innodb_data_fsyncs - number of fsync calls for data and log files
#
# * Innodb_log_writes - number of writes to the log file. These use buffered IO.
#
# * Innodb_os_log_fsyncs - number of fsync calls for the log file
#
# * Innodb_pages_read - number of reads done for data files.
#                       These include single-page reads done by per-connection threads,
#                       reads done by the main background thread during purge and
#                       insert buffer merges and reads done by the background IO threads.
#
# * Innodb_data_reads - number of reads for data and log files.
#                       Per-connection threads and the main background thread do reads in the size of an InnoDB page.
#                       The background IO threads can merge adjacent requests and do reads
#                       that are a multiple of the InnoDB page size.
#
# * Innodb_data_writes - number of writes for data and log files.
#                       Most writes are done by the background IO threads
#                       but in some cases per-connection threads request these writes
#                       and then block until they are done.
#                       This counter is incremented for the cheap log file writes
#                       that are a multiple of 512 bytes and use buffered IO,
#                       the frequently large writes to the double write buffer and the writes to the database files.
#                       The database file writes are a multiple of the InnoDB page size as write merging can be done.
#                       Some of the functions that request writes for dirty pages make it likely
#                       that write requests can be merged.
#                       Because this counter includes so many different types of writes
#                       it is not easy to reason about the amount of disk IO that is done for a given value.
#
# * Innodb_pages_written - the number of data file pages written.
#                           Writes to adjacent pages may be merged into a larger disk IO request.
#
# * Innodb_dblwr_pages_written - the number of data file pages written to the double write buffer.
#
# * Innodb_dblwr_writes - the number of disk writes done for the double write buffer.
#                         When the double write buffer is enabled,
#                         pages are first written to it sequentially using one large IO request
#                         before being updated in place.
