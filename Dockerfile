FROM ubuntu:latest
MAINTAINER Semara Incorporated


COPY requirements.txt ./
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE  8000

CMD [ "uwsgi", "main2.py" ]
