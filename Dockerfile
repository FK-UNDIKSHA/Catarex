FROM ubuntu:latest
MAINTAINER Semara Incorporated


COPY requirements.txt ./
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 python3-full python3-pip -y
RUN pip3 install virtualenv

RUN virtualenv env
RUN source env/bin/activate
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE  8000

CMD [ "env/source/bin/uwsgi", "main2.py" ]
