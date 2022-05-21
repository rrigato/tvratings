FROM amazonlinux:latest

RUN python --version

RUN yum -y groupinstall "Development Tools"

# RUN yum install -y wget gcc openssl-devel bzip2-devel libffi-devel 

RUN yum -y install wget

RUN cd /opt && wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz \
&& tar xzf Python-3.9.13.tgz && rm Python-3.9.13.tgz

RUN cd /opt/Python-3.9.13 && ./configure --enable-optimizations && make altinstall