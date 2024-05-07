from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Define choices for system roles
    Admin = 1
    Artist = 2
    normal_user = 3

    # Choices for gender
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    # Choices for user roles
    SYSTEM_ROLES = (
        (Admin, 'Admin'),
        (Artist, 'Artist'),
        (normal_user, 'Normal User'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True, max_length=1)
    profile = models.ImageField(upload_to="uploads/", null=True, blank=True)
    role = models.PositiveIntegerField(choices=SYSTEM_ROLES, default=normal_user)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'email']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
