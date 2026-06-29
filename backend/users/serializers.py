from rest_framework import serializers
from .models import User, WatchProgress


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'avatar', 'plan', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']


class WatchProgressSerializer(serializers.ModelSerializer):
    percent = serializers.ReadOnlyField()

    class Meta:
        model = WatchProgress
        fields = ['movie_id', 'position', 'duration', 'percent', 'updated_at']
