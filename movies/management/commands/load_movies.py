import json
import requests
import datetime
from django.core.management.base import BaseCommand
from ...models import Movie
from ...serializers import MovieSerializer

class Command(BaseCommand):
    help = 'Loads movies from a JSON file into the database, fetching additional details from an API.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing movie data.')

    def handle(self, *args, **options):
        json_file = options['json_file']
        with open(json_file, 'r') as f:
            movie_data = json.load(f)

        for movie in movie_data:
            # Extract movie ID from the current data
            movie_id = movie.get('id') 
             # Modify based on the actual ID field name in your JSON
            def convert_date_format(date_string):
                date = date_string.split('-')
                try:
                    yy = date[2]
                    mm = date[1]
                    dd = date[0]
                    date = f"{yy}-{mm}-{dd}"
                    return date 
                except:
                    return None
           

            # Check if movie ID exists
            if movie_id:
                try:
                    api_url = f'https://cinema.stag.rihal.tech/api/movie/{movie_id}'
                    response = requests.get(api_url)
                    response.raise_for_status()  # Raise an exception for non-200 status codes

                    api_data = response.json()
                    api_data['release_date'] = convert_date_format(api_data['release_date'])
                    api_data["main_cast"] = ",".join(api_data["main_cast"])
                    

                    # Combine data from JSON and API (modify as needed)
                    combined_data = {**movie, **api_data}

                    serializer = MovieSerializer(data=combined_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(f"Error creating movie (ID: {movie_id}): {serializer.errors}")
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching API data for movie ID {movie_id}: {e}")
            else:
                print(f"Skipping movie entry: Missing ID")

