#!/bin/sh

# Exit on error
set -e

# Debug (optional: helps in logs)
echo "Entrypoint started..."

# Allow direct alembic commands (for manual usage)
if [ "$1" = "alembic" ]; then
  exec "$@"
fi

# Wait for DB with retry + timeout safety
echo "Waiting for database at db:5432..."

RETRIES=30

until nc -z db 5432; do
  RETRIES=$((RETRIES - 1))
  if [ "$RETRIES" -le 0 ]; then
    echo "Database is not reachable. Exiting..."
    exit 1
  fi
  sleep 1
done

echo "Database is up"

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Seed DB (fail-safe)
echo "Seeding database..."
if python app/db/init_db.py; then
  echo "Seeding completed"
else
  echo "Seeding failed (continuing anyway)"
fi

# Start server
echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000