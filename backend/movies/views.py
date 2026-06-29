from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Movie, Genre
from .serializers import MovieListSerializer, MovieDetailSerializer, FeaturedMovieSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def featured(request):
    movie = Movie.objects.filter(is_featured=True).order_by('?').first()
    if not movie:
        movie = Movie.objects.order_by('?').first()
    return Response(FeaturedMovieSerializer(movie).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trending(request):
    movies = Movie.objects.filter(is_trending=True).order_by('?')[:20]
    return Response(MovieListSerializer(movies, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def new_releases(request):
    movies = Movie.objects.filter(is_new_release=True).order_by('-release_year')[:20]
    return Response(MovieListSerializer(movies, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_10(request):
    movies = Movie.objects.filter(is_top_10=True).order_by('top_10_rank')[:10]
    return Response(MovieListSerializer(movies, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def by_genre(request, genre_name):
    movies = Movie.objects.filter(
        genres__name__iexact=genre_name
    ).order_by('?')[:20]
    return Response(MovieListSerializer(movies, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):
    q = request.query_params.get('q', '').strip()
    if not q:
        return Response([])
    movies = Movie.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(cast__icontains=q) |
        Q(director__icontains=q) |
        Q(genres__name__icontains=q)
    ).distinct()[:30]
    return Response(MovieListSerializer(movies, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)
    return Response(MovieDetailSerializer(movie).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genres_list(request):
    genres = Genre.objects.all().order_by('name')
    from .serializers import GenreSerializer
    return Response(GenreSerializer(genres, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_rows(request):
    """Single endpoint that returns all home page rows."""
    rows = [
        {
            'id': 'trending',
            'title': 'Trending Now',
            'movies': MovieListSerializer(
                Movie.objects.filter(is_trending=True).order_by('?')[:18], many=True
            ).data,
        },
        {
            'id': 'top10',
            'title': 'Top 10 in India Today',
            'movies': MovieListSerializer(
                Movie.objects.filter(is_top_10=True).order_by('top_10_rank')[:10], many=True
            ).data,
        },
        {
            'id': 'new_releases',
            'title': 'New Releases',
            'movies': MovieListSerializer(
                Movie.objects.filter(is_new_release=True).order_by('-release_year')[:18], many=True
            ).data,
        },
        {
            'id': 'action',
            'title': 'Action & Adventure',
            'movies': MovieListSerializer(
                Movie.objects.filter(genres__name='Action').order_by('?')[:18], many=True
            ).data,
        },
        {
            'id': 'drama',
            'title': 'Award-Winning Dramas',
            'movies': MovieListSerializer(
                Movie.objects.filter(genres__name='Drama').order_by('?')[:18], many=True
            ).data,
        },
        {
            'id': 'scifi',
            'title': 'Sci-Fi & Fantasy',
            'movies': MovieListSerializer(
                Movie.objects.filter(genres__name='Sci-Fi').order_by('?')[:18], many=True
            ).data,
        },
        {
            'id': 'comedy',
            'title': 'Comedy',
            'movies': MovieListSerializer(
                Movie.objects.filter(genres__name='Comedy').order_by('?')[:18], many=True
            ).data,
        },
        {
            'id': 'documentary',
            'title': 'Documentaries',
            'movies': MovieListSerializer(
                Movie.objects.filter(genres__name='Documentary').order_by('?')[:18], many=True
            ).data,
        },
    ]
    # Filter out empty rows
    rows = [r for r in rows if r['movies']]
    return Response(rows)
