FROM python:3.11-slim

LABEL maintainer="john.doe@example.com"
LABEL version="1.0"
LABEL description="Wine quality predictor"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data .
COPY train_model.py .

RUN mkdir models

ENTRYPOINT ["python", "train_model.py"]
