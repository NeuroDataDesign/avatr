FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python-setuptools python-dev python-pip build-essential
RUN mkdir /workdirectory
ADD "./test.py" "./"
ADD "./boutiques.json" "./"

WORKDIR /workdirectory/
