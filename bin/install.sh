#!/usr/bin/env bash

sudo -u postgres psql <<EOF
CREATE DATABASE django_plato_assets;
CREATE USER django WITH PASSWORD 'django_password';
GRANT ALL PRIVILEGES ON DATABASE django_plato_assets TO django;
ALTER USER django CREATEDB;
EOF

pip3 install -r requirements.txt
python3 manage.py migrate
