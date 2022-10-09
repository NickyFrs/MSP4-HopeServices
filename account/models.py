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

        email = self.normalize_email(email) # validation of email format
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    # login details
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(max_length=500, blank=True)

    # user address. for delivery purposes
    mobile = models.CharField(max_length=15, blank=True)
    address_l1 = models.CharField(max_length=200, blank=True)
    address_l2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    post_code = models.CharField(max_length=12, blank=True)
    # country = models.CharField(max_length=50, default='United Kingdom', blank=True)
    country = CountryField()

    # User status. use for accont verification
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('Accounts')
        verbose_name_plural = _('Accounts')

    def email_to_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username
