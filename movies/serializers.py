from django.db.models import Avg
from django.contrib.humanize.templatetags.humanize import intword

from rest_framework import serializers
from num2words import num2words
import math

from .models import Movie,MovieRating,Memory

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'  # Include all fields by default



class MovieRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = MovieRating
        fields = ('rating',)

    def validate(self, attrs):
        """
        Custom validation to ensure rating is within the valid range.
        """
        if not (1 <= attrs['rating'] <= 10):
            raise serializers.ValidationError('Rating must be between 1 and 10')
        return attrs
    
class MoviesSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description']

class MoviesSerializerWithRating(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'average_rating']

    def get_average_rating(self, obj):
        return MovieRating.objects.filter(movie=obj).aggregate(Avg('rating'))['rating__avg']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Truncate description to 100 characters
        if len(rep['description']) > 100:
            rep['description'] = rep['description'][:100].rsplit(' ', 1)[0] + '...'
        return rep
    


class MovieDetailSerializer(serializers.ModelSerializer):
    budget_in_words = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    my_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'release_date', 'main_cast', 'director', 'budget',
                'budget_in_words', 'my_rating', 'average_rating']



    def get_budget_in_words(self, obj):
         return num2words(obj.budget).capitalize()

    def get_average_rating(self, obj):
        return MovieRating.objects.filter(movie=obj).aggregate(Avg('rating'))['rating__avg']

    def get_my_rating(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            user_rating = MovieRating.objects.filter(movie=obj, user=request.user).first()
            if user_rating:
                return user_rating.rating
        return None
    
    
class MemorySerializer(serializers.ModelSerializer):
    movie_id = serializers.ReadOnlyField(source='movie.id')
    movie_name = serializers.ReadOnlyField(source='movie.name')

    class Meta:
        model = Memory
        fields = ['id', 'movie_id', 'movie_name', 'title']

class CreateMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['movie', 'title', 'date', 'photos', 'story']




class MemoryDetailSerializer(serializers.ModelSerializer):
    movie_id = serializers.ReadOnlyField(source='movie.id')
    movie_name = serializers.ReadOnlyField(source='movie.name')
    # photo_id = serializers.ReadOnlyField(source='photos.id', allow_null=True)
    photo_name = serializers.ReadOnlyField(source='photos.name', allow_null=True)
    photo_extension = serializers.SerializerMethodField()
    photo_size = serializers.SerializerMethodField()
    # time_created = serializers.ReadOnlyField(source='memory.time_created', allow_null=True)
    class Meta:
        model = Memory
        fields = ['id', 'movie_id', 'movie_name', 'title', 'story', 'photo_name', 'photo_extension', 'photo_size', 'time_created']

    def get_photo_extension(self, obj):
        photos = obj.photos
        if photos:
            return photos.name.split('.')[-1]
        return ''

    def get_photo_size(self, obj):
        photos = obj.photos
        if photos:
            size = photos.size
            if size == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size, 1024)))
            p = math.pow(1024, i)
            s = round(size / p, 2)
            return "%s%s" % (s, size_name[i])
        return ''
    

class UpdateMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['title', 'story']




# class PhotoDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = ['id', 'name', 'extension', 'size', 'time_created']

#     def get_photo_size(self, obj):
#         size = obj.size
#         if size == 0:
#             return "0KB"
#         size_in_kb = round(size / 1024, 2)  # Convert bytes to kilobytes
#         return "%sKB" % size_in_kb
    
# class MemoryDetailSerializer(serializers.ModelSerializer):
#     movie_id = serializers.ReadOnlyField(source='movie.id')
#     movie_name = serializers.ReadOnlyField(source='movie.name')
#     photos = PhotoDetailsSerializer(many=True, read_only=True)

#     class Meta:
#         model = Memory
#         fields = ['id', 'movie_id', 'movie_name', 'title', 'story', 'photos']

# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = ['id', 'image']

# class MemoryCreateSerializer(serializers.ModelSerializer):
#     photos = PhotoSerializer(many=True, required=False)

#     class Meta:
#         model = Memory
#         fields = [ 'movie', 'title', 'date', 'story', 'photos']

#     def create(self, validated_data):
#         photos_data = validated_data.pop('photos', [])
#         memory = Memory.objects.create(**validated_data)
#         for photo_data in photos_data:
#             Photo.objects.create(memory=memory, **photo_data)
#         return memory
    


# class MemoryUpdatePhotosSerializer(serializers.ModelSerializer):
#     photos = PhotoSerializer(many=True, required=False)

#     class Meta:
#         model = Memory
#         fields = ['photos']

#     def update(self, instance, validated_data):
#         photos_data = validated_data.pop('photos', [])
#         for photo_data in photos_data:
#             Photo.objects.create(memory=instance, **photo_data)
#         return instance
# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = ['image']

# class MemoryCreateSerializer(serializers.ModelSerializer):
#     photos = PhotoSerializer(many=True, required=False)

#     class Meta:
#         model = Memory
#         fields = [ 'movie', 'title', 'date', 'story', 'photos']

#     def create(self, validated_data):
#         photos_data = validated_data.pop('photos', [])
#         memory = Memory.objects.create(**validated_data)
#         for photo_data in photos_data:
#             Photo.objects.create(memory=memory, **photo_data).save()
#         return memory