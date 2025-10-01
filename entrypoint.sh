#!/bin/sh

echo "Starting Django application..."

# Create db directory if it doesn't exist
mkdir -p /app/db

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: username=admin, password=admin123')
else:
    print('ℹ️  Superuser already exists')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Django application ready!"

# Start server
exec "$@"
