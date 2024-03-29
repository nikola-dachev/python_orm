from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager


# Create your models here.


class Person(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')


class Director(Person):
    years_of_experience = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])

    objects = DirectorManager()


class Actor(Person):
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    # class GenreChoices(models.TextChoices):
    #     ACTION = 'Action',
    #     COMEDY = 'Comedy',
    #     DRAMA = 'Drama',
    #     OTHER = 'Other'

    GENRE_CHOICES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other')
    )

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=6, default='Other', choices=GENRE_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=1,default= 0.0,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    starring_actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True,blank= True, related_name='movies')
    actors = models.ManyToManyField(Actor)

