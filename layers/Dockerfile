FROM amazonlinux:latest

RUN python --version

RUN yum -y groupinstall "Development Tools"

RUN yum install -y wget 

# RUN yum install python39

RUN cd /opt 


RUN wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz 

RUN tar xzf Python-3.9.13.tgz

RUN cd Python-3.9.13

# RUN ./configure --enable-optimizations