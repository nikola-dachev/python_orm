
from django.db import models

from main_app.custom_validators import all_digits
from django.core.validators import MinLengthValidator, MinValueValidator
from main_app.custom_manager import AstronautManager

# Create your models here.

class Astronaut(models.Model):
    name = models.CharField(max_length=120,
                            validators = [MinLengthValidator(2)])
    phone_number = models.CharField(max_length=15, unique= True,
                                    validators = [all_digits])
    is_active = models.BooleanField(default= True)
    date_of_birth = models.DateField(null= True, blank= True)
    spacewalks= models.IntegerField(validators =[MinValueValidator(0)], default =0)
    updated_at = models.DateTimeField(auto_now= True)

    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(max_length=120,
                            validators=[MinLengthValidator(2)])
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])
    weight= models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now= True)

class Mission(models.Model):

    STATUS_CHOICES = (
        ("Planned", "Planned"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed")
    )
    name = models.CharField(max_length=120,
                            validators=[MinLengthValidator(2)])
    description = models.TextField(null= True, blank = True)
    status = models.CharField(max_length= 9, choices = STATUS_CHOICES, default = "Planned" )
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now= True)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name="missions")
    astronauts = models.ManyToManyField(Astronaut, related_name="missions")
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL, related_name="commander_mission", null = True, blank= True)


