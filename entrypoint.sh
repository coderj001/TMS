#!/bin/sh

RED='\033[0;31m'
RED='\032[0;31m'
NC='\033[0m'

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --no-input
echo -e "${GREEN} LMS Migration ${NC}"
python manage.py flush --no-input
echo -e "${GREEN} LMS Migration ${NC}"
python manage.py migrate
# echo -e "${GREEN} LMS Testcase ${NC}"
# python manage.py test -v 3


exec "$@"
