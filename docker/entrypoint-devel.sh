#!/bin/sh
cd /opt/waikup

# wait for database and mail server
dockerize -wait "tcp://db:5432" \
          -wait "tcp://mta:25" \
          -timeout 30s

# install application dependencies
pipenv install -d

# setup database
PGUSER=postgres PGPASSWORD=postgres psql -h db <<EOQUERY
CREATE USER waikup WITH PASSWORD 'waikup' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE DATABASE waikup-devel WITH OWNER waikup;
EOQUERY
pipenv run python manage.py setupdb

# serve application
uwsgi --socket 0.0.0.0:5000 \
      --protocol uwsgi \
      --master \
      --processes 4 \
      --threads 2 \
      --plugins python \
      --virtualenv $(pipenv --venv) \
      --python-autoreload 1 \
      --wsgi waikup.app:app
