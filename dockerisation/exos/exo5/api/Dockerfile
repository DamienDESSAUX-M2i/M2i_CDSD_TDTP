FROM python:3.11-slim

LABEL maintainer="john.doe@example.com"
LABEL version="1.0"
LABEL description="Predictor"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd -m appuser
USER appuser

ENTRYPOINT ["python", "app.py"]