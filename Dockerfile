FROM python:3.10.10-slim-bullseye
WORKDIR /sipi
COPY ./sipi_back .
COPY ./requirements.txt .
COPY ./start.sh .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
VOLUME /sipi/static

WORKDIR /sipi

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "sipi_back.wsgi:application"]

