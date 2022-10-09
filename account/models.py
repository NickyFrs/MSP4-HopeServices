from email.policy import default
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django_countries.fields import CountryField
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

# Models from here.


class CustomAccountManager(BaseUserManager):

    # create a superuser/admin user account
    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have set is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have set is_superuser=True')

        return self.create_user(email, username, password, **other_fields)

    # create a normal user account
    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You most provide a valid email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
