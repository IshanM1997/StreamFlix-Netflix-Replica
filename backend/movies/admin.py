from django.contrib import admin
from .models import Movie, Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'content_type', 'is_featured', 'is_trending', 'is_top_10', 'top_10_rank']
    list_filter = ['content_type', 'is_featured', 'is_trending', 'is_new_release', 'is_top_10', 'genres']
    search_fields = ['title', 'description', 'cast', 'director']
    filter_horizontal = ['genres']
    list_editable = ['is_featured', 'is_trending', 'is_top_10', 'top_10_rank']
    ordering = ['-created_at']
