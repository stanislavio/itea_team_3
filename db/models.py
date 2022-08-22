from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,)
from django_countries.fields import CountryField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Create and return a `User` with an email, phone number, username and password.
        """
        if not email:
            raise ValueError("Users must have an email.")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if not password:
            raise ValueError("Superusers must have a password.")
        if not email:
            raise ValueError("Superusers must have an email.")

        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email address')
    username = models.CharField(db_index=True, max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="users", null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=80)
    height = models.DecimalField(max_digits=5, decimal_places=2, default=180)
    phone = models.CharField(max_length=15, null=True, blank=True)
    country = CountryField()
    city = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    object = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Workouts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_workout = models.CharField('Название тренировки', max_length=50)
    date_create = models.DateTimeField('Дата теренировки', auto_now_add=True)
    exercise_name = models.CharField('Название упражнения', max_length=50)
    number_of_approaches = models.IntegerField('Количество подходов')
    amount_of_exercise = models.IntegerField('Количество упражнений')
    distance = models.DecimalField('Пройденая дистанция', max_digits=5, decimal_places=2)
    workout_time = models.DecimalField('Время тренировки', max_digits=5, decimal_places=2)
    photo_workout = models.ImageField('Фото тренировки', upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField('Описание тренировки')

    def __str__(self):
        return self.name_workout

    @property
    def photo_url(self):
        if self.photo_workout and hasattr(self.photo_workout, 'url'):
            return self.photo_workout.url

