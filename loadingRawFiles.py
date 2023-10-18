import os
from hdfsFunctions import *

#datasets = ["https://www.kaggle.com/datasets/hgultekin/bbcnewsarchive",
            #"https://www.kaggle.com/datasets/ishikajohari/best-books-10k-multi-genre-data",
            #"https://www.kaggle.com/datasets/arshkon/linkedin-job-postings",
            #"https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions"]

'''
This script writes our raw data into our Hadoop server in HDFS.
'''
hdfs_path = "/rawFiles"
deleteHdfsFolder(hdfs_path)
createHdfsDirectory(hdfs_path)
for i in os.listdir("./datasets"):
    print(f"Uploading {i} in HDFS...")
    uploadToHdfs("./datasets/"+str(i),hdfs_path)


