import binascii, os
from datetime import datetime, timedelta
from collections import namedtuple

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

from user.constants import TOKEN_EXPIRY_TIME
from base.models import BaseModel


class UserManager(BaseUserManager):
    """
    This is my custom user manager 
    """

    def get_first_name(self, name):
        return name.split(' ')[0]

    def _create_user(self, email, first_name, password, gender, **extra_fields):
        """
        It will create user with entered email and password
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        if not first_name:
            raise ValueError('First Name is mandatory')
        if not gender:
            raise ValueError('Gender is mandatory')
        
        first_name = self.get_first_name(first_name)
        user = self.model(email=email, first_name=first_name, gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, password, gender, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = True
        return self._create_user(email, first_name, password, gender, **extra_fields)

    def create_superuser(self, email, first_name, password, gender, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self._create_user(email, first_name, password, gender, **extra_fields)


class UserInfo(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    This model stores user related information
    """
    OPTION = namedtuple('OPTION',['MALE','FEMALE'])(
        MALE=1,
        FEMALE=2
        )
    GENDER_OPTION = [
        (OPTION.MALE, 'MALE'),
        (OPTION.FEMALE, 'FEMALE')]

    email = models.EmailField(verbose_name="Email Id", max_length=255, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50)
    password = models.CharField(verbose_name="Password", max_length=128)
    gender = models.PositiveIntegerField(verbose_name="Gender", choices=GENDER_OPTION)
    email_token = models.CharField(max_length=255, null=True, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','gender']

    objects = UserManager()

    def __str__(self):
        return "{} : {}".format(self.first_name, self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class Token(BaseModel, models.Model):
    """
    This model will store token which will be used to authenticate user
    """
    key = models.CharField(unique=True, max_length=255, verbose_name="Token Key")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True)
    expiry_time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.expiry_time = datetime.now() + timedelta(hours=TOKEN_EXPIRY_TIME)
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
