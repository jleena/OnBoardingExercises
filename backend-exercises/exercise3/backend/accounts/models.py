from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

class MyUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The user must have an email addrsess")
        email = self.normalize.email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    id: uuid.UUID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name: str = models.CharField(max_length=255)
    email: str = models.EmailField(unique=True)
    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = BaseUserManager()

    def __str__(self) -> str:
        return self.email