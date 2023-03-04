FROM python:3.10.10-slim-bullseye
WORKDIR /sipi
COPY ./sipi_back .
COPY ./requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install tree -y


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /sipi

RUN pwd
RUN tree

CMD ["pwd"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "sipi_back.wsgi:application"]

