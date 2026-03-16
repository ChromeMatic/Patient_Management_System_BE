#!/bin/bash

set -e

echo "Waiting to connect to database...."

until nc -z "$DB_HOST" "$DB_PORT"; do
    echo "Waiting for database connection.."
    sleep 3
done

echo "Database up and running"

alembic upgrade head

echo "Starting Backend Service..."

exec gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 60