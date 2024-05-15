#!/bin/sh
set -e

echo "Sleeping for 10 seconds to allow Postgres to start..."
sleep 10

echo "Postgres should be up - continuing..."
exec "$@"