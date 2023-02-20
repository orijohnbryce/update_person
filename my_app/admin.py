from django.contrib import admin

# Register your models here.

from .models import Car, Person, Rent


admin.site.register(Car)
admin.site.register(Person)
admin.site.register(Rent)
