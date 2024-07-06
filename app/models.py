from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, username, password, user_type):
        user = self.model(
            email=email,
            username=username,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            user_type="Admin"
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractUser):
    USER_TYPE = (
        ('User', 'User'),
        ('Security', 'Security'),
        ('Admin', 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, default='')
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='User')

    objects = UserManager()

    def __str__(self):
        return self.username

class Visitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor_name = models.CharField(max_length=100, default='Unknown')
    visitor_email = models.EmailField(max_length=255, blank=True, default='')
    visitor_phone = models.CharField(max_length=15, blank=True, default='')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator_type = models.CharField(max_length=50)  # 'user' or 'visitor'
    creator_id = models.CharField(max_length=255)  # user ID or visitor name
    
    def __str__(self):
        return self.title 


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    