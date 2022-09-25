#!/bin/sh

if [ "$DATABASE" = "postgresql" ]
then
    echo ">>> WAITING FOR POSTGRESQL DATABASE"
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done
    echo ">>> POSTGRESQL DATABASE STARTED"
fi

echo ">>> EXECUTING $@"
exec "$@"