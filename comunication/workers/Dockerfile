FROM ubuntu
MAINTAINER Micol
ADD MLFV.zip /home/
EXPOSE 18810
RUN apt-get update && apt-get install -y zip && apt-get install -y unzip
RUN cd home/ && unzip MLFV.zip && cd MLFV/
WORKDIR home/MLFV/
RUN apt-get install -y python2.7 &&  apt-get install -y  python-pip && pip install scikit-learn==0.20.0 && pip install rpyc && pip install pandas && apt-get clean
ENTRYPOINT python init_client.py
