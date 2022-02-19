FROM ubuntu:18.04

RUN apt-get update

WORKDIR /root/

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get install -y --no-install-recommends \
    vim \
    wget \
    build-essential

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
&& rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install setuptools
RUN python3 -m pip install uwsgi flask requests

WORKDIR /home/chall/service

CMD uwsgi --http 0.0.0.0:6666 --chdir ro/ --master --module wsgi --processes 4