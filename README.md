# DataIntensive
The code is split in two parts: 
1. First part consist of the ingestion of data into our Big Data architecture.
You should be able to do that by running our bash script [run.sh](run.sh).
2. Second part is related with the processing part and the implementation of a ML classifier.
This part can bu seen in our [processing.ipynb](processing.ipynb) notebook.

There are some requirements first to run each of the files.

### Architecture
The architecture should be ready but sometimes the server fails and we need to reboot the system, so first of all:

Be sure the server is running:
```{bash}
ping 54.211.123.215
```
If it is not, ask us to restart the instance from AWS or prepare your own virtual machine with [this](https://drive.google.com/file/d/1oOavxhvV4ff9x_nDtEWsZFGBiZGe6sxv/view?usp=drivesdk) image.
If that is the case, remember to modify the following files by changing the old IP (54.211.123.215) by the new IP address:
```
nano /usr/local/hadoop/etc/hadoop/core-site.xml
nano /usr/local/hadoop/etc/hadoop/yarn-site.xml
nano /usr/local/hadoop/etc/hadoop/mapred-site.xml
nano /usr/local/hbase/conf/hbase-site.xml
```

When it is running, be sure Hadoop is running properly:
http://54.211.123.215:9870

If it is not, then connect to the server via SSH and start Hadoop, HBase and thrift daemons:
```{bash}
ssh -i "ID2221keys.pem" ubuntu@ec2-54.211.123.215.compute-1.amazonaws.com
./start-all.sh
hdfs dfs -mkdir /processedDatasets/bbc-news-data.csv
hdfs dfs -mkdir /processedDatasets/goodreads_data.csv
hdfs dfs -mkdir /processedDatasets/job_postings.csv
hdfs dfs -mkdir /processedDatasets/mtsamples.csv
hdfs dfs -mkdir /dataSets

```
**_NOTE_**: You will need the **keys** (ID2221keys.pem) to access the instance through SSH. You will find the keys in our zip file.

Now you should be ready to run the ingestion code: [run.sh](run.sh)
```
curl -fL https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz | gzip -d > cs && chmod +x cs && ./cs setup
sudo apt install python3-pip
pip install jupyter
coursier launch --fork almond:0.10.9 -- --install
```

### Processing
For the processing part, you would need to have Scala installed as well as a Scala kernel for Jupyter notebooks:

Install Scala by following [this site](https://www.scala-lang.org/download/).
Install the Scala kernel for Jupyter Notebook: 

```{bash}
sudo apt-get install libzmq3-dev
git clone https://github.com/alexarchambault/jupyter-scala.git
cd jupyter-scala
sbt cli:packArchive
./jupyter-scala
```

You should be able to run the scripts now:
Just run [this script](processing.ipynb).

 

