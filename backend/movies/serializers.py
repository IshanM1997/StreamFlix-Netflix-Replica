from rest_framework import serializers
from .models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for rows/grids"""
    genre_names = serializers.ReadOnlyField()
    duration_label = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'slug', 'content_type',
            'poster_url', 'backdrop_url',
            'release_year', 'maturity_rating', 'duration_label',
            'match_score', 'genre_names', 'is_top_10', 'top_10_rank',
            'is_new_release', 'short_description',
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    """Full serializer for modal / detail view"""
    genre_names = serializers.ReadOnlyField()
    duration_label = serializers.ReadOnlyField()
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'content_type', 'genres', 'genre_names',
            'backdrop_url', 'poster_url', 'logo_url',
            'release_year', 'maturity_rating', 'duration_label', 'duration_minutes',
            'cast', 'director', 'language',
            'video_url', 'trailer_url',
            'is_featured', 'is_trending', 'is_top_10', 'top_10_rank',
            'match_score', 'imdb_rating',
        ]


class FeaturedMovieSerializer(serializers.ModelSerializer):
    """For hero banner — needs all rich fields"""
    genre_names = serializers.ReadOnlyField()
    duration_label = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'backdrop_url', 'poster_url', 'logo_url',
            'genre_names', 'release_year', 'maturity_rating',
            'duration_label', 'match_score', 'trailer_url',
        ]
