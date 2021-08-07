release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn TaxManagementSystem.wsgi:application --log-file -
