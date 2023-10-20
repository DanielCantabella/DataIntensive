from hdfs import InsecureClient
import configparser
CONFIG_ROUTE = './config.cfg'

"""
This script contains different functions to connect with HDFS in order to upload and remove data.
"""

def get_server_data(cfgFileDirectory):
    """
    Get the hadoop server info (host, port, user) we are using in our project (contained in config.cfg file).
    :param cfgFileDirectory: path of the config.cfg file containing server info.
    :return: host, port, user
    """
    config = configparser.ConfigParser()
    config.read(cfgFileDirectory)
    host = config.get('hadoop_server', 'host')
    port = config.get('hadoop_server', 'port')
    user = config.get('hadoop_server', 'user')
    return host, port, user

def checkIfExistsInHDFS(HDFSpath):
    '''
    Check if a path/file exists in HDFS.
    :param HDFSpath: HDFS path/file you want to check if exists.
    :return: True if the path already exists in HDFS, False if not.
    '''
    host, port, user = get_server_data(CONFIG_ROUTE)
    client = InsecureClient("http://" + host + ":" + port + "/", user=user)
    if client.status(HDFSpath, strict=False):
        return True
    else:
        return False

def sendToHdfs(filePath, hdfsPath, n_threads: int = 1):
    '''
    Sends the file to HDFS.
    :param filePath: local file directory
    :param hdfsPath: hdfs directory
    :param n_threads: number of threads to use when uploading a file to HDFS
    '''
    host, port, user = get_server_data(CONFIG_ROUTE)
    hdfs_client = InsecureClient("http://" + host + ":" + port + "/", user=user)
    hdfs_client.upload(hdfsPath, filePath, n_threads=n_threads)


def uploadToHdfs(filePath, hdfsPath, n_threads: int = 1):
    '''
    Uploads the file to HDFS if it doesn't exists yet.
    :param filePath: local file directory
    :param hdfsPath: hdfs directory
    :param n_threads:
    :return:
    '''
    if not checkIfExistsInHDFS(hdfsPath):
        print(f"File '{filePath}' already in HDFS at '{hdfsPath}'")
    else:
        sendToHdfs(filePath, hdfsPath, n_threads=n_threads)
        print(f"File '{filePath}' uploaded in HDFS at '{hdfsPath}'")


def deleteHdfsFolder(HDFSfolder):
    '''
    Deletes the HDFS folder if it exists
    :param HDFSfolder: path to the folder to be deleted
    '''
    host, port, user = get_server_data(CONFIG_ROUTE)
    client = InsecureClient("http://" + host + ":" + port + "/", user=user)

    if client.status(HDFSfolder, strict=False):
        client.delete(HDFSfolder, recursive=True)
        print(f"Folder {HDFSfolder} has been overwritten in HDFS")
    else:
        pass

def createHdfsDirectory(hdfs_path):
    '''
    Tries to create a new hdfs folder
    :param hdfs_path: path to the folder to be created
    '''
    try:
        host, port, user = get_server_data(CONFIG_ROUTE)
        client = InsecureClient("http://" + host + ":" + port + "/", user=user)
        # Check if the directory already exists
        if not client.status(hdfs_path, strict=False):
            # If it doesn't exist, create the directory
            client.makedirs(hdfs_path)
        print(f"Directory '{hdfs_path}' created in HDFS.")
    except Exception as e:
        print(f"Error: {str(e)}")