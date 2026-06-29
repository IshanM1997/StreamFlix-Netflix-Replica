from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=120)
    avatar = models.CharField(max_length=10, default='🎬')
    plan = models.CharField(
        max_length=20,
        choices=[('standard', 'Standard'), ('premium', 'Premium'), ('basic', 'Basic')],
        default='premium'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


class WatchProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    movie_id = models.CharField(max_length=36)
    position = models.FloatField(default=0)     # seconds watched
    duration = models.FloatField(default=0)     # total duration
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'watch_progress'
        unique_together = ('user', 'movie_id')

    @property
    def percent(self):
        if self.duration <= 0:
            return 0
        return round((self.position / self.duration) * 100, 1)


class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_list')
    movie_id = models.CharField(max_length=36)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'my_list'
        unique_together = ('user', 'movie_id')
