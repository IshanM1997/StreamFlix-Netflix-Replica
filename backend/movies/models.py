from django.db import models
import uuid


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return self.name


class Movie(models.Model):
    CONTENT_TYPES = [('movie', 'Movie'), ('series', 'Series'), ('documentary', 'Documentary')]
    MATURITY_RATINGS = [('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('TV-MA', 'TV-MA'), ('TV-14', 'TV-14')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='movie')
    genres = models.ManyToManyField(Genre, related_name='movies')

    # Images (TMDB-style URLs for seeded data)
    backdrop_url = models.URLField(max_length=500)
    poster_url = models.URLField(max_length=500)
    logo_url = models.URLField(max_length=500, blank=True)

    # Metadata
    release_year = models.IntegerField()
    maturity_rating = models.CharField(max_length=10, choices=MATURITY_RATINGS, default='PG-13')
    duration_minutes = models.IntegerField(default=120)
    cast = models.JSONField(default=list)
    director = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=10, default='en')

    # Streaming info
    video_url = models.URLField(max_length=500, blank=True)   # placeholder stream URL
    trailer_url = models.URLField(max_length=500, blank=True)

    # Flags for home row curation
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_new_release = models.BooleanField(default=False)
    is_top_10 = models.BooleanField(default=False)
    top_10_rank = models.IntegerField(null=True, blank=True)

    # Stats
    match_score = models.IntegerField(default=95)   # % match shown to user
    imdb_rating = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'movies'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def duration_label(self):
        h, m = divmod(self.duration_minutes, 60)
        return f"{h}h {m}m" if h else f"{m}m"

    @property
    def genre_names(self):
        return list(self.genres.values_list('name', flat=True))
