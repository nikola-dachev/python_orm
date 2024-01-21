from datetime import date

from django.db import models



# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)


class Department(models.Model):

    DEPARTMENT_CHOICES = [
        ("Sofia", "Sofia"),
        ("Plovdiv", "Plovdiv"),
        ("Varna", "Varna"),
        ("Burgas", "Burgas")
    ]

    code = models.CharField(max_length=4, primary_key=True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveIntegerField("Employees Count", default = 1)
    location = models.CharField(max_length= 20, blank=True, null=True, choices=DEPARTMENT_CHOICES)
    last_edited_on = models.DateTimeField(auto_now=True, editable= False)


class Project(models.Model):
    name = models.CharField(max_length=100, unique= True)
    description = models.TextField(blank= True, null= True)
    budget= models.DecimalField(max_digits=10, decimal_places= 2, blank= True, null= True)
    duration_in_days =models.PositiveIntegerField("Duration in Days", blank= True, null= True)
    estimated_hours = models.FloatField("Estimated Hours", blank= True, null= True)
    start_date = models.DateTimeField("Start Date", blank= True, null= True, default = date.today)
    created_on = models.DateTimeField(auto_now_add=True, editable= False)
    last_edited_on = models.DateTimeField(auto_now=True, editable= False)