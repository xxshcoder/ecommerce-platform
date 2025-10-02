#!/bin/sh

echo "Waiting for PostgreSQL to start..."

# Wait for PostgreSQL
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started! 🐘"

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

echo "✅ Setup complete! Starting server..."

# Execute the main command
exec "$@"