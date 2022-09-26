# Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """ Manager for users profile """
    
    def create_user(self, email, username, name, last_name, password):
        """ Create a new user profile """
        if not email:
            raise ValueError("The user must have an email")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            name=name,
            last_name=last_name
            )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, username, name, last_name):
        """ Create a new superuser """
        user = self.create_user(
            email=email,
            username=username,
            name=name,
            last_name=last_name,
            password=password
            )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Base model for users """
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    username = models.CharField(
        max_length=20,
        unique=True
        )
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    def __str__(self):
        return self.username