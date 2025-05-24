FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY transaction_service/ /app/transaction_service/

ENV PYTHONPATH=/app

CMD ["uvicorn", "transaction_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
