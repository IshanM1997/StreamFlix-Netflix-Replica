from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users import views as user_views
from movies import views as movie_views

urlpatterns = [
    # Auth
    path('auth/register/', user_views.RegisterView.as_view(), name='register'),
    path('auth/login/', user_views.login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', user_views.profile_view, name='profile'),

    # Profile
    path('profile/', user_views.profile_view, name='profile_update'),

    # Movies
    path('movies/featured/', movie_views.featured, name='featured'),
    path('movies/trending/', movie_views.trending, name='trending'),
    path('movies/new-releases/', movie_views.new_releases, name='new_releases'),
    path('movies/top-10/', movie_views.top_10, name='top_10'),
    path('movies/genre/<str:genre_name>/', movie_views.by_genre, name='by_genre'),
    path('movies/search/', movie_views.search, name='search'),
    path('movies/home-rows/', movie_views.home_rows, name='home_rows'),
    path('movies/genres/', movie_views.genres_list, name='genres'),
    path('movies/<uuid:movie_id>/', movie_views.movie_detail, name='movie_detail'),

    # My List
    path('my-list/', user_views.my_list_view, name='my_list'),
    path('my-list/<str:movie_id>/', user_views.my_list_toggle, name='my_list_toggle'),
    path('my-list/<str:movie_id>/status/', user_views.my_list_status, name='my_list_status'),

    # Watch progress / continue watching
    path('continue-watching/', user_views.continue_watching, name='continue_watching'),
    path('watch-progress/<str:movie_id>/', user_views.update_progress, name='update_progress'),
]
