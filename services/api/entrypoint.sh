#!/bin/sh

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "-----------------------------------------------------"
if [ "$DATABASE" = "postgresql" ]
then
    echo ">>> ${BLUE}WAITING FOR POSTGRESQL DATABASE${NC}"
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done
    echo ">>> ${GREEN}POSTGRESQL DATABASE STARTED${NC}"
fi
echo "-----------------------------------------------------"
echo ">>> ${BLUE} EXECUTING $@${NC}"
exec "$@"