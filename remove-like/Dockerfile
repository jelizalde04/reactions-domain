
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6002

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "6002", "--reload"]