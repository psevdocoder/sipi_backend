FROM python:3.10.10-slim-bullseye
WORKDIR /sipi
COPY ./sipi_back .
COPY ./requirements.txt .
COPY ./start.sh .
COPY ./fixtures.json .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh

EXPOSE 8000
VOLUME /sipi/logs
VOLUME /sipi/static

WORKDIR /sipi

CMD ["./start.sh"]

