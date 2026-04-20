FROM python:3.11-slim

LABEL maintainer="votre.email@example.com"
LABEL version="1.0"
LABEL description="Analyse des ventes"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.csv .
COPY analyse.py .

RUN useradd -m appuser
USER appuser

ENTRYPOINT ["python", "analyse.py"]
CMD ["data.csv"]
