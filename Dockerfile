FROM python:3.11-alpine

LABEL author="Meysam Azad <meysam@licenseware.io>"

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install -Ur requirements.txt pip

COPY main.py .
ENTRYPOINT ["/main.py"]
