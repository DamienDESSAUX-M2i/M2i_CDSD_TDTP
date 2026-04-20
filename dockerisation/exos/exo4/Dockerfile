FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configuration par défaut
ENV ENVIRONMENT=development
ENV MODEL_TYPE=logistic
ENV N_ESTIMATORS=100
ENV TEST_SIZE=0.2
ENV RANDOM_STATE=42
ENV LOG_LEVEL=INFO
ENV ENABLE_MONITORING=false
ENV DATA_PATH=/app/data/dataset.csv
ENV MODEL_OUTPUT=/app/models/
ENV N_SAMPLES=1000
ENV N_FEATURES=20

COPY advanced_trainer.py .

CMD ["python", "advanced_trainer.py"]