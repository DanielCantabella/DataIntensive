
#pip install toree
#jupyter toree install --spark_home=/usr/local/bin/apache-spark/
#jupyter toree install --spark_opts='--master=local[4]'
#brew install sbt

#sudo su
#echo "54.211.123.215 hadoop" >> /etc/hosts
#echo "54.211.123.215 ip-172-31-95-96.ec2.internal" >> /etc/hosts

python loadingRawFiles.py
python loadDatalake.py



