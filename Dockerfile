FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /filmbook
COPY requirements.txt /filmbook/
RUN pip install -r requirements.txt
COPY . /filmbook

