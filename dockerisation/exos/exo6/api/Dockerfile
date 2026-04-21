FROM python:3.11-slim

LABEL maintainer="john.doe@example.com"
LABEL version="1.0"
LABEL description="Wine quality predictor"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY database.py .
COPY train.py .

ENTRYPOINT ["python", "app.py"]