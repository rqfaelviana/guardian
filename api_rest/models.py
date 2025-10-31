from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):

    def create_user(self, email: str, first_name: str, last_name: str, password: str = None, is_staff=False,
                    is_superuser=False, **extra_fields):

        if not email:
            raise ValueError('O campo Email é obrigatório')
        if not first_name:
            raise ValueError("O campo Primeiro Nome é obrigatório")
        if not last_name:
            raise ValueError("O campo Último Nome é obrigatório")
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff 
        user.is_superuser = is_superuser 
        user.save(using=self._db)
        return user


    def create_superuser(self, email: str, first_name: str, last_name: str, password: str = None,):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.is_staff = True

        return user

class Cliente(AbstractUser):

    username = None


    first_name = models.CharField(verbose_name='primeiro nome', max_length=150, blank=False)
    last_name = models.CharField(verbose_name='último nome', max_length=150, blank=False)

    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email