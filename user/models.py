import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from user.usermanager import (
    AdminManager,
    TaxAccountantManager,
    TaxPayerManager,
    UserManager
)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    email = models.EmailField(
        unique=True,
        null=False,
        verbose_name="Email"
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        verbose_name="Username"
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Last Name'
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type_choice = (
        ('admin', 'ADMIN'),
        ('tax-payer', 'TAX-PAYER'),
        ('tax-accountant', 'TAX-ACCOUNTANT')
    )
    user_type = models.CharField(
        max_length=14,
        choices=user_type_choice,
        default='admin'
    )

    objects = UserManager()
    adminmanager = AdminManager()
    taxpayermanager = TaxPayerManager()
    taxaccountantmanager = TaxAccountantManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_username(self):
        return f"{self.username}"

    def __str__(self):
        return str(self.username)
