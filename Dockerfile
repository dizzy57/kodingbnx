FROM python:3.8

RUN apt-get update -y && apt-get install -y expect wait-for-it && python -m venv /venv
WORKDIR /app

COPY requirements.txt dev-requirements.txt ./
RUN /venv/bin/pip install pip-tools && /venv/bin/pip-sync requirements.txt dev-requirements.txt
