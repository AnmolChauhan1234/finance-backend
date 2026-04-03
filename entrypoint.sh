#!/bin/sh

echo "⏳ Waiting for database..."

while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Database is up"

# Only run migrations if alembic exists
if [ -d "alembic" ]; then
  alembic upgrade head
else
  echo "⚠️ Alembic not initialized, skipping migrations"
fi

python app/db/init_db.py

uvicorn app.main:app --host 0.0.0.0 --port 8000