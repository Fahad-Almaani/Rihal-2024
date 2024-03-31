from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Movie(models.Model):
    # Id id default
    name = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField(null=True)
    main_cast = models.CharField(max_length=500, blank=True)
    director = models.CharField(max_length=255,null=True)
    budget = models.IntegerField(null=True)
    

class MovieRating(models.Model):
    """Model for storing movie ratings by users."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to User model
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Link to Movie model
    rating = models.PositiveIntegerField(choices=((i, i) for i in range(1, 11)))  # Rating from 1 to 10

    class Meta:
        """Unique constraint on user and movie combination."""
        unique_together = (('user', 'movie'),)