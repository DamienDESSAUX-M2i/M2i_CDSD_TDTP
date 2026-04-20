FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train_simple.py .

ENTRYPOINT ["python", "train_simple.py"]