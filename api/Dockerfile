FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Обновите pip перед установкой зависимостей
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
