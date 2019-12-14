FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get -y install python3-pip

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY bot.py bot.py

CMD python3 bot.py
