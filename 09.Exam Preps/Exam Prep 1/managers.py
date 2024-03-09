from django.db import models
from django.db.models import Count


# Create your tests here.
class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(movies_count= Count('movies')).order_by('-movies_count', 'full_name')