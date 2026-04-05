#!/usr/bin/env bash
set -e

pip install -r requirements.txt
cd server
python manage.py collectstatic --noinput
python manage.py migrate
