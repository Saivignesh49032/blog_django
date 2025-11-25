import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblogproject.settings')
django.setup()

from blog.models import Category

categories = ['General', 'Anime', 'Technology', 'Lifestyle', 'Programming', 'Gaming', 'Movies']

for cat_name in categories:
    cat, created = Category.objects.get_or_create(name=cat_name)
    if created:
        print(f'Created category: {cat_name}')
    else:
        print(f'Category already exists: {cat_name}')
