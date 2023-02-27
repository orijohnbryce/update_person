import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_prj.settings")


import django
django.setup()

from my_app.models import Car
from django.contrib.auth.models import User


print(User.objects.all())

u = User.objects.create_user(username="shimi", password="123")





