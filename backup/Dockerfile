FROM ubuntu:16.04

WORKDIR /root/

RUN apt-get update && apt-get install -y libc6-dev-i386 python python-pip build-essential socat 
RUN pip install nclib==0.8.3

RUN useradd -ms /bin/bash --uid 31337 chall
USER chall
WORKDIR /home/chall

CMD cd service/rw && socat tcp-l:6666,reuseaddr,fork exec:"../ro/backup" 
