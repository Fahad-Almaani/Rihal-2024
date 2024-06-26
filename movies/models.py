from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Movie(models.Model):
    # Id id default
    name = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField(null=True,blank=True)
    main_cast = models.CharField(max_length=500, blank=True)
    director = models.CharField(max_length=255,null=True,blank=True)
    budget = models.IntegerField(null=True,blank=True)
    def __str__(self) -> str:
        return self.name
    

class MovieRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to User model
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Link to Movie model
    rating = models.PositiveIntegerField(choices=((i, i) for i in range(1, 11)))  # Rating from 1 to 10

    class Meta:
        unique_together = (('user', 'movie'),)



class Memory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to User model
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Link to Movie model
    title = models.CharField(max_length=255)
    photos = models.ImageField(upload_to='memory_photos/',null=True,blank=True)
    date = models.DateField()
    story = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.movie.name}"


# class Photo(models.Model):
#     memory = models.ForeignKey(Memory, related_name='photos', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='memory_photos/')