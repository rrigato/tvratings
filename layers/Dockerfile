FROM amazonlinux:latest

ARG BUILT_LAYER_NAME

ENV PYTHON_VERSION="3.9.13"

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
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar xzf Python-$PYTHON_VERSION.tgz && \
    rm Python-$PYTHON_VERSION.tgz

#python install
RUN cd /opt/Python-$PYTHON_VERSION && \ 
    ./configure --enable-optimizations && make altinstall

RUN python3.9 -m venv avenv

COPY requirements/ requirements/

#ask-sdk-core install
RUN source avenv/bin/activate && \
    mkdir python && \
    pip install -r requirements/requirements-ask-layer.txt --target ./python 

#bundle dependency for deployment as layer
RUN zip -r $BUILT_LAYER_NAME python
