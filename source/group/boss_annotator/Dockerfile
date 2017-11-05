# existing image build
FROM ubuntu:16.04

#installing pip and essentials
RUN apt-get update
RUN apt-get -y install python3-setuptools python3-dev python3-pip build-essential vim nano

RUN pip3 install slacker>=0.9.50 boto3>=1.4.6 intern==0.9.4 tailer>=0.4.1 numpy>=1.13.1 Pillow>=4.2.1 blosc==1.4.4 mock==2.0.0 nose2==0.6.5 pbr==3.1.1 requests==2.11.1 six==1.10.0 scikit-image

RUN mkdir /workdirectory

WORKDIR /workdirectory

RUN mkdir DATA
ADD ./ ./

WORKDIR /workdirectory
CMD ["/bin/bash"]
