FROM python:3.11-slim

LABEL maintainer="john.doe@example.com"
LABEL version="1.0"
LABEL description="Wine quality predictor frontend"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]