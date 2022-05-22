FROM amazonlinux:latest

RUN yum install -y tar \
    wget \
    gcc \
    openssl-devel \
    bzip2-devel \
    libffi-devel \
    gzip \
    make \
    zip

#python3 download
RUN cd /opt && \
    wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz && \
    tar xzf Python-3.9.13.tgz && \
    rm Python-3.9.13.tgz

#python install
RUN cd /opt/Python-3.9.13 && \ 
    ./configure --enable-optimizations && make altinstall

RUN python3.9 -m venv avenv

COPY requirements/ requirements/

#ask-sdk-core install
RUN source avenv/bin/activate && \
    mkdir python && \
    pip install -r requirements/requirements-ask-layer.txt --target ./python 

#bundle dependency for deployment as layer
RUN zip -r ask_layer.zip python
