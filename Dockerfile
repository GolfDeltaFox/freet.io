FROM python:3.6.4

EXPOSE 80

RUN apt-get update

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD python main.py
