FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    curl \
    pip \
    unzip \
    python
    
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN pip3 install numpy pandas matplotlib

ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""

COPY . /costVisulization
WORKDIR "/costVisulization"
RUN /bin/bash ./s_main.sh