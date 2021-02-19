from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, tg_id, **extra_fields):
        """Creates and saves a new user"""
        user = self.model(tg_id=tg_id, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_superuser(self, tg_id):
        """Creates and saves a new superuser"""
        user = self.create_user(tg_id)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model supports Telegram ID instead of username"""
    tg_id = models.CharField(max_length=255, unique=True, default='')
    first_name = models.CharField(max_length=255, default='')
    second_name = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=255, default='')
    language_code = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'tg_id'
