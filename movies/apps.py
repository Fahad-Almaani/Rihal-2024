from django.apps import AppConfig
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from .management.commands import load_movies
from django.conf import settings
import os
# from django.core.management import call_command

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    # def ready(self):
    #     from django.core.management import call_command
    #     json_file_path = os.path.join(settings.BASE_DIR, 'movies', 'movies_data', 'movies.json')
    #     call_command('load_movies', json_file_path)
    # @receiver(post_migrate)
    # def load_movies_after_migration(sender, **kwargs):
    #     """Loads movies from JSON after database migrations are applied."""
    #     json_file_path = os.path.join(settings.BASE_DIR, 'movies', 'movies_data', 'movies.json')
    #     call_command('load_movies', json_file_path)