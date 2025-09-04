from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from tasks.models import Category, Priority, Task, SubTask, Note

class Command(BaseCommand):
    help = "Seed database with Categories, Priorities, Tasks, SubTasks, and Notes"

    def handle(self, *args, **options):
        fake = Faker()

        for name in ["Work", "School", "Personal", "Finance", "Projects"]:
            Category.objects.get_or_create(name=name)

        for name in ["Critical", "High", "Medium", "Low", "Optional"]:
            Priority.objects.get_or_create(name=name)

        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())
        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5), 
                description=fake.paragraph(nb_sentences=3), 
                status=fake.random_element(elements=statuses),
                deadline=timezone.make_aware(
                    fake.date_time_this_month()
                ),
                priority=random.choice(priorities),
                category=random.choice(categories),
            )

            for _ in range(random.randint(1, 3)):
                Note.objects.create(task=task, content=fake.paragraph(nb_sentences=2))

            for _ in range(random.randint(0, 5)):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=statuses),
                )

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete."))