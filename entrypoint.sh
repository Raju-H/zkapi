#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

if [ -z "$(python manage.py shell -c 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email="$SUPER_USER_EMAIL").exists()')" ]; then
    DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --email $SUPER_USER_EMAIL --noinput
fi

gunicorn appcore.wsgi:application --bind 0.0.0.0:8000