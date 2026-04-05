#!/bin/sh
set -e

# Allow running alembic commands directly
if [ "$1" = "alembic" ]; then
  exec "$@"
fi

echo "⏳ Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Database is up"

echo "📦 Running migrations..."
alembic upgrade head

echo "🌱 Seeding database..."
python app/db/init_db.py

echo "🚀 Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
