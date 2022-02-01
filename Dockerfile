FROM datamechanics/spark:3.2-latest

USER root
RUN apt-get update && apt-get --assume-yes install build-essential && pip install --upgrade pip
USER 185

ENV PYSPARK_MAJOR_PYTHON_VERSION=3
WORKDIR /opt/application/

COPY .env .
COPY requirements.txt .
RUN pip install  -r requirements.txt 
   


ADD site-packages site-packages
