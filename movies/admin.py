from django.contrib import admin
from .models import Movie, MovieRating,Memory

# Register your models here
admin.site.register(Movie)
admin.site.register(MovieRating)
admin.site.register(Memory)