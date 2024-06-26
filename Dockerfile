FROM ubuntu:latest
MAINTAINER Semara Incorporated


COPY . .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 python3-full python3-pip -y

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

EXPOSE  8000

CMD [ "uwsgi", "uwsgi.ini" ]
