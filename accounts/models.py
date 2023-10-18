from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, firstName, lastName, email, password=None):
        if not email:
            raise ValueError('Email is required')

        user = self.model(
            firstName=firstName,
            lastName=lastName,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstName, lastName, email, password=None):
        user = self.create_user(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    firstName = models.CharField(max_length=255, verbose_name="firstName")
    lastName = models.CharField(max_length=255, verbose_name="lastName")

    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name="email address"
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    dateJoined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
