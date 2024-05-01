FROM shosoar/alpine-python-opencv
MAINTAINER Semara Incorporated


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE  8000

CMD [ "uwsgi", "main2.py" ]
