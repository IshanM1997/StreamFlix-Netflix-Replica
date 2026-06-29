from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, WatchProgress, MyList

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'plan', 'is_active', 'date_joined']
    list_filter = ['plan', 'is_active', 'is_staff']
    search_fields = ['email', 'name']
    ordering = ['-date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Profile', {'fields': ('name', 'avatar', 'plan')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'name', 'password1', 'password2')}),
    )

@admin.register(WatchProgress)
class WatchProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie_id', 'position', 'duration', 'updated_at']
    list_filter = ['updated_at']

@admin.register(MyList)
class MyListAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie_id', 'added_at']
