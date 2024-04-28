from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom model manager for User model with no email field
    """

    use_in_migrations = True
    
    def _create_user(self, username, password, **extra_fields):
        """Create and save a User with given username and password"""
        if not username:
            raise ValueError('Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, password=None, **extra_fields):
        """Create and save regular User with the given username and password"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)
    
    def create_superuser(self, username, password, **extra_fields):
        """Create and save a SuperUser with the given username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model w\o email field.

    Username and password are required. Other fields are optional.
    """
    last_name = None
    email = None
    photo = models.ImageField('Изображение профиля', upload_to='avatars', default='avatars/nophoto.jpg')
    REQUIRED_FIELDS = []
    objects = UserManager()
