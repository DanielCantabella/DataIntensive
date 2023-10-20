from datetime import datetime
MAX_CHUNK_SIZE = 9 * 1024 * 1024  # 9 MB

"""
This script contains different functions to upload HDFS files to HBase .
"""
def create_table_if_not_exists(connection, table):
    if table.encode() not in connection.tables():
        connection.create_table(table, {'data': dict()})
        print(f"Table {table} has been created in HBase.")

def uploadFilesInHbase(hdfs_client, hdfs_path, table, fileListPath):
    '''
    This function checks the hdfs directory and checks if it contains a file.
    If it is a file, it loads it into Hbase.
    If it is a directory, it checks if it contains files and does the same.
    :param hdfs_client: HDFS client
    :param hdfs_path: root path from where you want to start uploading the files
    :param table: HBase table connection
    :param fileListPath: file containing entries in HBase
    '''
    files = hdfs_client.list(hdfs_path)
    for entry in files:
        entry_path = hdfs_path + "/" + entry
        status = hdfs_client.status(entry_path)

        if status['type'] == 'FILE':
            print(f"{entry_path} is a file")
            read_raw_and_insert_hbase(hdfs_client, table, entry_path, fileListPath)
            print("Uploaded to HBase")
        elif status['type'] == 'DIRECTORY':
            print(f"{entry_path} is a directory")
            # Recursively list files within the sub-directory
            uploadFilesInHbase(hdfs_client, entry_path, table, fileListPath)
        else:
            print(f"{entry_path} is of an unknown type")

def read_raw_and_insert_hbase(client, table, hdfs_path, fileListPath):
    '''
    This function uploads the file in "hdfs_path" in table "table" (which must have a column family called "data").
    It uploads it in "data:raw" column family.
    The row (aka key) it assigns corresponds to: sourceOfTheFile$fileFormat$rawFileName$modificationTime.
    The value is the raw data itself.
    NOTE: As we only use Kaggle data our sourceOfTheFile is "kaggle" every time we find a file.
    We also load the file in different chunks since our key-value maxSize limit is 10MB, smaller than our files.
    :param client: HDFS client
    :param table: HBase table connection
    :param hdfs_path: HDFS path of the file
    :param fileListPath: file containing entries in HBase
    '''
    # generate key
    source = "kaggle"
    format = hdfs_path.split('.')[1]
    file_name = hdfs_path.split('.')[0].split('/')[-1]

    status = client.status(hdfs_path)
    modification_time_milliseconds = status["modificationTime"]
    mtime = str(datetime.fromtimestamp(modification_time_milliseconds / 1000.0))
    mtime = mtime.replace(' ','-')

    row_key = '$'.join([source, format, file_name, mtime])
    chunk_keys = []
    # Read the file from HDFS
    with client.read(hdfs_path) as f:
        while True:
            # Read a chunk of data
            chunk = f.read(MAX_CHUNK_SIZE)
            if not chunk:
                break  # End of file
            # Create a unique row key for each chunk (e.g., append a chunk index)
            chunk_key = f"{row_key}${len(chunk)}"
            chunk_keys.append(chunk_key)
            # Insert the chunk into HBase
            row_value = {'data:raw': chunk}
            table.put(chunk_key, row_value)

    with open(fileListPath, 'a') as txt_file:
        for chunk_key in chunk_keys:
            txt_file.write(chunk_key + '\n')