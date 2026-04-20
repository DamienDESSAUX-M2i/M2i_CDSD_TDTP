FROM python:3.11-slim

WORKDIR /app

COPY generate_data.py .

RUN mkdir data_output

ENTRYPOINT ["python", "generate_data.py"]