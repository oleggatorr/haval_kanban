FROM python:3.11-slim

WORKDIR /app

# Добавляем postgresql-client для утилиты pg_isready
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY wheels/ ./wheels/
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=./wheels -r requirements.txt

COPY . .

# Копируем и делаем исполняемым наш скрипт запуска
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Указываем entrypoint. "$@" передаст команду из CMD
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]