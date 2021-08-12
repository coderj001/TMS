from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        if not username:
            raise ValueError('The given username must be set')

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        # Its not nessery for form creating user
        extra_fields.setdefault('is_staff', True)

        return self._create_user(
            email,
            username,
            password,
            **extra_fields
        )

    def create_tax_payer(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'tax-payer')

        return self.create_user(
            email,
            username,
            password,
            **extra_fields
        )

    def create_tax_accountant(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'tax-accountant')

        return self.create_user(
            email,
            username,
            password,
            **extra_fields
        )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email,
            username,
            password,
            **extra_fields
        )


class AdminManager(models.Manager):
    def get_queryset(self):
        return super(AdminManager, self).get_queryset().filter(user_type='admin')


class TaxPayerManager(models.Manager):
    def get_queryset(self):
        return super(TaxPayerManager, self).get_queryset().filter(user_type='tax-payer')


class TaxAccountantManager(models.Manager):
    def get_queryset(self):
        return super(TaxAccountantManager, self).get_queryset().filter(user_type='tax-accountant')
