FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train.py .
RUN python train.py

COPY app.py .

ENV MLFLOW_TRACKING_URI="sqlite:///mlflow.db"
ENV MODEL_NAME="iris-api-model"
ENV MODEL_STAGE="Production"

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
