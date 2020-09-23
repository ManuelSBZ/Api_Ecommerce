#!/bin/sh

flask db init
flask db migrate -m "initial migration"
flask db upgrade

gunicorn entrypoint:app -w 2 --threads 2 -b 0.0.0.0:5000

exec "$@"