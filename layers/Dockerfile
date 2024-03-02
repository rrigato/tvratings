# Make sure to use the amazonlinux version appropriate to python version 
# of the operating system documented here:
# https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
FROM amazonlinux:2

ARG BUILT_LAYER_NAME

ENV PYTHON_VERSION="3.11.8"

# note that openssl-devel since it is version openssl v3.x.x 
# is not compatiable with python 3.11.8
# The below installs openssl v1.x.x
RUN yum install -y tar \
    wget \
    gcc \
    openssl11-devel \
    openssl11 \
    bzip2-devel \
    libffi-devel \
    gzip \
    make \
    zip


# python3 download
RUN cd /opt && \
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar xzf Python-$PYTHON_VERSION.tgz && \
    rm Python-$PYTHON_VERSION.tgz

#python install
RUN cd /opt/Python-$PYTHON_VERSION && \ 
    ./configure --enable-optimizations && make altinstall


RUN /opt/Python-$PYTHON_VERSION/python -m venv avenv

COPY requirements/ requirements/

# #ask-sdk-core install
RUN source avenv/bin/activate && \
    mkdir python && \
    pip install -r requirements/requirements-dev.txt --target ./python 

#bundle dependency for deployment as layer
RUN zip -r $BUILT_LAYER_NAME python
