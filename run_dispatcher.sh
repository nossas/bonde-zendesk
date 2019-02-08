#!/bin/sh
WORKERS=${WORKERS:5}

pg-dispatcher --db-uri="$DATABASE_URL" --redis-uri="$REDIS_URL" --channel="$DB_CHANNEL" --workers="$WORKERS" --exec="python main.py"
