# Надежная версия Python (рекомендуется 3.12, не 3.13!)
FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

RUN apt-get remove -y build-essential && apt-get autoremove -y && apt-get clean

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
