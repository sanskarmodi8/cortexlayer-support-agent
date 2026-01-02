#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

until python - <<EOF
import psycopg2
import os
try:
    psycopg2.connect(os.environ["DATABASE_URL"])
    print("PostgreSQL is ready")
except Exception as e:
    raise SystemExit(1)
EOF
do
  sleep 2
done

echo "Running DB migrations..."
cd backend
alembic upgrade head

echo "Starting application..."
exec "$@"
