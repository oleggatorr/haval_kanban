#!/bin/sh

# Ждем, пока база данных станет доступна
echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U ${DB_USER}; do
  sleep 1
done
echo "Database is ready!"

# Применяем миграции Alembic
echo "Running database migrations..."
alembic upgrade head

# Запускаем основное приложение (переданные аргументы)
echo "Starting application..."
exec "$@"