from django.db import models
from django.contrib.auth.models import AbstractUser
from.managers import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=80)
    phone_no = models.CharField(unique=True, max_length=14)
    # is_verifed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return f"{self.email} {self.phone_no}"


    def generate_activation_token(self):
        token_generator = PasswordResetTokenGenerator()
        self.activation_token = token_generator.make_token(self)
        self.save(update_fields=["activation_token"])

        