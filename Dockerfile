FROM python:3.8

WORKDIR /notify
RUN sudo apt-get install libgl1-mesa-glx
COPY requirements.txt /notify/
RUN pip3 install -r requirements.txt
COPY . /notify/

CMD python3 channelnotifier.py
