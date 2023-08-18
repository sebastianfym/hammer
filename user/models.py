import random
import string

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, Group)
from django.db import models
from django.db import transaction
from django.utils import timezone


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def _create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The given phone number must be set')
        try:
            with transaction.atomic():
                user = self.model(phone_number=phone_number, **extra_fields)
                if password:
                    user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, phone_number,  **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, **extra_fields)


    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone_number, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_groups'  # Добавить это поле
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Разрешения пользователя',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_permissions'  # Добавить это поле
    )
    phone_number = models.CharField(max_length=12, blank=True, null=True, verbose_name='Номер телефона', unique=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='Инвайт-код')
    invite_code_for_users = models.CharField(max_length=6, blank=True, null=True,
                                             verbose_name='Инвайт-код для пользователей')

    is_active = models.BooleanField(default=True, verbose_name="активный")
    is_staff = models.BooleanField(default=False, verbose_name="персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="админ")
    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    def __str__(self):
        return f'{self.phone_number}, {self.invite_code}, {self.invite_code_for_users}'

    @property
    def invited_users(self):
        return User.objects.filter(invite_code_for_users=self.invite_code_for_users)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
