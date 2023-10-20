import happybase
from hdfs import InsecureClient
import configparser
import os
from hbaseFunctions import *

#Loads config environment
CONFIG_ROUTE = 'config.cfg'
config = configparser.ConfigParser()
config.read(CONFIG_ROUTE)
host = config.get('hadoop_server', 'host')
user = config.get('hadoop_server', 'user')
portHdfs = config.get('hadoop_server', 'port')
hdfs_path = config.get('routes', 'hdfs')
portHbase = config.get('hbase', 'port')
tablename = config.get('hbase', 'tablename')
hbaseFileListPath = config.get('hbase', 'fileListPath')

#Resets the hbaseFileList
if os.path.exists(hbaseFileListPath):
    os.remove(hbaseFileListPath)
    print(f"{hbaseFileListPath} has been removed.")

# Connect to hdfs
hdfs_client = InsecureClient("http://" + host + ":" + portHdfs + "/", user=user)

# Connect to HBase and opload the files
connection = happybase.Connection(host=host, port=int(portHbase))
connection.open()
create_table_if_not_exists(connection,tablename)
table = connection.table(tablename)
uploadFilesInHbase(hdfs_client, hdfs_path, table, hbaseFileListPath)
connection.close()



