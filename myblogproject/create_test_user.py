import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblogproject.settings')
django.setup()

User = get_user_model()
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user('testuser', 'test@example.com', 'password123')
    print("Created user: testuser")
else:
    print("User testuser already exists")
