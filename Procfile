release: python manage.py migrate
web: gunicorn SalonVuala.wsgi:application --bind 0.0.0.0:$PORT
