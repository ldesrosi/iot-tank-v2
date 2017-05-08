FROM ubuntu:latest
MAINTAINER Luc Desrosiers "ldesrosi73@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libopencv-dev python-opencv

COPY ./requirements.txt /
RUN pip install -r requirements.txt

#COPY ./geventlet.py.patch /usr/local/lib/python2.7/dist-packages/gunicorn/workers/geventlet.py
