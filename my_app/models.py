from django.db import models

# Create your models here.


class Car(models.Model):
    car_type = models.CharField(max_length=20, null=False)
    year = models.PositiveIntegerField(null=True, blank=True)
    plate_number = models.IntegerField(null=True, blank=True)

    renters = models.ManyToManyField("Person", through="Rent",
                                     null=True, blank=True,
                                     related_name="rented_cars")

    owner = models.ForeignKey('Person', on_delete=models.RESTRICT,
                              related_name="car_owner", null=True)

    def __str__(self):
        return self.car_type


class Rent(models.Model):
    car = models.ForeignKey("Car", on_delete=models.RESTRICT)
    person = models.ForeignKey("Person", on_delete=models.RESTRICT)

    sdate = models.DateTimeField(auto_now=True)
    edate = models.DateTimeField(null=True, blank=True)


class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name






