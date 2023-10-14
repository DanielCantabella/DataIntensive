# DataIntensive
Be sure the server is running:
```{bash}
ping 35.175.92.154
```
If it is not, ask me (Dani) to restart the instance from AWS.

If it is running, be sure Hadoop is running properly:
http://35.175.92.154:9870

If it is not, then connect to the server via SSH and start Hadoop daemons:
```{bash}
ssh -i "ID2221keys.pem" ubuntu@ec2-35-175-92-154.compute-1.amazonaws.com
./start-hadoop.sh
```
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
Just run [this script](run.sh).

 

