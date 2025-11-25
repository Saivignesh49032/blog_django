import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblogproject.settings')
django.setup()

from polls.models import Question, Choice

# Check if a poll exists
if not Question.objects.exists():
    q = Question.objects.create(question_text="What is your favorite programming language?", pub_date=timezone.now())
    Choice.objects.create(question=q, choice_text="Python")
    Choice.objects.create(question=q, choice_text="JavaScript")
    Choice.objects.create(question=q, choice_text="Rust")
    Choice.objects.create(question=q, choice_text="Go")
    print(f"Created poll: {q.question_text}")
else:
    print("Poll already exists")
