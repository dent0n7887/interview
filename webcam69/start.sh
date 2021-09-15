#!/bin/sh

nohup celery -A celery_app.celery_app worker -l info &

nohup celery -A celery_app.celery_app flower &

gunicorn -c gunicorn.py webcam_app:webcam_app
