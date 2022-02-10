FROM datamechanics/spark:3.2-latest

USER root
RUN apt-get update 
RUN  apt-get --assume-yes install build-essential openssh-server sudo vim-tiny &&  pip install --upgrade pip
RUN useradd -rm -s /bin/bash -g root -G sudo -u 1000 test
RUN  echo 'test:test' | chpasswd
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER test

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

WORKDIR /opt/application/

COPY .env .
COPY requirements.txt .
RUN pip install  -r requirements.txt 

USER root
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4
USER test
   
ADD site-packages site-packages
