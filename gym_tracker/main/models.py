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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Training(models.Model):
    """
    Training session model.
    """
    name = models.CharField('Название', max_length=40)
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
    
    def __str__(self) -> str:
        return f'{self.owner.first_name} - {self.name}'


class Exercise(models.Model):
    """
    The exercise model of a training.
    """
    name = models.CharField('Название', max_length=40)
    training = models.ForeignKey(to=Training, on_delete=models.CASCADE, related_name='exercises')

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
    
    def __str__(self) -> str:
        return f'{self.name} - {self.training.name}'


class FinishedTraining(models.Model):
    """
    Training session start and end times model.
    """
    training = models.ForeignKey(to=Training, on_delete=models.CASCADE, related_name='finished_trainings')
    started_at = models.DateTimeField('Старт', blank=True, null=True)
    finished_at = models.DateTimeField('Финиш', blank=True, null=True)

    class Meta:
        verbose_name = 'Выполненная тренировка'
        verbose_name_plural = 'Выполненные тренировки'
        ordering = ('-started_at', )

    
    def __str__(self) -> str:
        return f'{self.training.name} - {self.started_at}-{self.finished_at}'


class FinishedExerciseSet(models.Model):
    """
    Completed exercise set stats.
    """
    training = models.ForeignKey(to=FinishedTraining, on_delete=models.CASCADE)
    exercise = models.ForeignKey(to=Exercise, on_delete=models.CASCADE)
    set = models.PositiveSmallIntegerField('Подход')
    weight = models.PositiveSmallIntegerField('Вес', null=True)
    repetitions = models.PositiveSmallIntegerField('Повторений')

    class Meta:
        verbose_name = 'Выполненный подход'
        verbose_name_plural = 'Выполненные подходы'

