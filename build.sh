#!/usr/bin/env bash
set -e

pip install -r server/requirements.txt
python server/manage.py collectstatic --noinput
python server/manage.py migrate
