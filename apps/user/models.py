import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    fio = models.CharField(max_length=100, null=False)
    email = models.EmailField(_('email address'), unique=True, null=False)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    is_admin = models.BooleanField(default=False)
    balance = models.IntegerField(null=False, default=0)
    spent_balance = models.IntegerField(null=False, default=0)

    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'phone_number']

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class IndividualUser(models.Model):
    ip_name = models.CharField(max_length=255, null=True)
    iin = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='individual_user')


class JuridicalUser(models.Model):
    company_name = models.CharField(max_length=255, null=True)
    bin = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='juridical_user')
    swift = models.CharField(max_length=255, null=True)
    kbe = models.CharField(max_length=255, null=True)
    iban = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    post_address = models.CharField(max_length=255, null=True)
    official_address = models.CharField(max_length=255, null=True)


class EmployeeUser(models.Model):
    position = models.CharField(max_length=255, null=True)
    juridical = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child_juridical')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employee_user')


class UserVerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=255, null=False)
