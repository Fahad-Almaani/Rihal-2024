
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters

from .models import Movie , MovieRating,Memory
from .serializers import *

import re
from collections import Counter
import string
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords
from Levenshtein import distance


nltk.download('stopwords')
        
class MovieRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_pk):
        """
        Create a rating for a specific movie by the authenticated user.

        Request Body:
        {
            "rating": (Integer between 1 and 10)
        }
        """
        
        try:
            movie = Movie.objects.get(pk=movie_pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if user has already rated this movie
        if MovieRating.objects.filter(user=request.user, movie=movie).exists():
            return Response({'error': 'You have already rated this movie'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure rating is within the valid range (1-10)
        rating = serializer.validated_data['rating']
        if not (1 <= rating <= 10):
            return Response({'error': 'Rating must be between 1 and 10'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, movie_pk):
        """
        Retrieve the average rating for a specific movie.
        """

        try:
            movie = Movie.objects.get(pk=movie_pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        ratings = MovieRating.objects.filter(movie=movie)
        if not ratings.exists():
            return Response({'average_rating': None})  # Handle no ratings case

        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        return Response({'average_rating': round(average_rating, 2)})  # Round to 2 decimal places
    

class GetAllMovies(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        movies = Movie.objects.all()
        serializer = MoviesSerializerWithRating(movies,many=True)

        return Response(serializer.data)


class MovieDetailAPIView(APIView):
    def get(self, request, movie_pk):
        movie = Movie.objects.filter(id=movie_pk).first()  # Get the movie instance by ID
        if movie:
            serializer = MovieDetailSerializer(movie, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"message": "Movie not found"}, status=404)
        
        
class MovieSearchAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class TopRatedMoviesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.annotate(avg_rating=Avg('movierating__rating')).order_by('-avg_rating')[:5]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class CreateMemoryAPIView(generics.CreateAPIView):
    
    serializer_class = CreateMemorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyMemoriesAPIView(generics.ListAPIView):
    serializer_class = MemorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Memory.objects.filter(user=user)
    

class MemoryDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Memory.objects.all()
    serializer_class = MemoryDetailSerializer
    lookup_field = 'id'

class MemoryPhotoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, memory_id):
        memory = get_object_or_404(Memory, id=memory_id)
        photo = memory.photos

        # Return the photo as a file response
        if photo:
            try:
                return FileResponse(photo, content_type='image/jpeg')
            except Exception as e:
                return Response(str(e), status=500)
        else:
            return Response("Photo not found", status=404)

class UpdateMemoryAPIView(generics.UpdateAPIView):
    queryset = Memory.objects.all()
    serializer_class = UpdateMemorySerializer
    permission_classes = [IsAuthenticated]

class DeleteMemoryAPIView(generics.DestroyAPIView):
    queryset = Memory.objects.all()
    permission_classes = [IsAuthenticated]


class TopWordsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        # Get all stories from memories
        stories = Memory.objects.exclude(story__isnull=True).values_list('story', flat=True)

        # Combine stories into a single string
        all_text = ' '.join(stories)

        # Remove punctuation and convert to lowercase
        all_text = all_text.translate(str.maketrans('', '', string.punctuation)).lower()

        # Tokenize text
        words = all_text.split()

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]

        # Count occurrences of each word
        word_counts = Counter(words)

        # Get top 5 words
        top_words = word_counts.most_common(5)

        return Response(top_words)
    

class ExtractURLsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, memory_id):
        memory = get_object_or_404(Memory, id=memory_id)
        story = memory.story

        # Regular expression pattern to match URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

        # Find all URLs in the story using regex
        urls = re.findall(url_pattern, story)

        return Response(urls)
    


def calculate_similarity(self, query):
    """
    Calculates a similarity score between the movie name and the search query.

    Args:
        query (str): The search query provided by the user.

    Returns:
        float: A similarity score between 0 (no similarity) and 1 (exact match).
    """

    # 1. Lowercase both strings for case-insensitive comparison
    movie_name_lower = self.name.lower()
    query_lower = query.lower()

    # 2. Calculate Levenshtein distance (minimum edits needed to transform one string to another)
    levenshtein_distance = distance(movie_name_lower, query_lower)

    # 3. Calculate normalized score based on Levenshtein distance and (optionally) name length
    name_length = len(movie_name_lower)
    max_distance = max(len(movie_name_lower), len(query_lower))  # Consider longer string length

    # Adjust weights (w1 and w2) and normalization factors as needed based on your data and preferences
    w1 = 0.8  # Weight for Levenshtein distance
    w2 = 0.2  # Weight for name length (optional)
    normalized_score = 1 - (w1 * levenshtein_distance / max_distance + w2 * abs(name_length - len(query_lower)) / name_length)

    return normalized_score

class GuessMovieAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('query', '')
       
        if not query:
            return Response({'detail': 'Please provide a search query.'}, status=400)

        # Leverage database filtering for efficient search:
        filtered_movies = Movie.objects.filter(name__icontains=query)

        # Prioritize exact matches:
        exact_matches = filtered_movies.filter(name__iexact=query)  # Case-insensitive exact match
        if exact_matches:
            return Response({
                'movies': [movie.serialize() for movie in exact_matches]
            })

        return Response(exact_matches)
      

        return Response({'detail': 'No movies found matching your query.'}, status=404)
    

class CompareRatingsAPIView(APIView):
    def get(self, request):
        # Get the current user
        User = get_user_model()
        current_user = request.user

        # Fetch user ratings for the current user
        user_ratings = MovieRating.objects.filter(user=current_user).values('movie__name', 'rating')

        # Calculate average ratings for all movies
        average_ratings = MovieRating.objects.values('movie__name').annotate(avg_rating=Avg('rating'))

        # Create a dictionary to store average ratings
        avg_ratings_dict = {rating['movie__name']: rating['avg_rating'] for rating in average_ratings}

        # List to store movie ratings
        movie_ratings = []

        # Iterate over user ratings
        for user_rating in user_ratings:
            movie_name = user_rating['movie__name']
            user_rating_value = user_rating['rating']

            # Get the corresponding average rating
            avg_rating_value = avg_ratings_dict.get(movie_name)

            # Determine if user rating matches average rating
            is_matching = user_rating_value == avg_rating_value

            # Add movie rating to list
            movie_ratings.append({
                'movie_name': movie_name,
                'my_rating': user_rating_value,
                'avg_rating': avg_rating_value,
                'is_matching': is_matching
            })

        return Response(movie_ratings)