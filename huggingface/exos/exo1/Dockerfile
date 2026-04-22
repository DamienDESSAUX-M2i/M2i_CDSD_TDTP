# Builder
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/.venv

ENV PATH="/opt/.venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from transformers import pipeline; pipeline('text-classification', model='papluca/xlm-roberta-base-language-detection');"

# Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /opt/.venv /opt/.venv

COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

COPY app.py .

ENV PATH="/opt/.venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["python", "app.py"]