from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, usdt_address, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not usdt_address:
            raise ValueError("Users must have a USDT address")
        user = self.model(
            email=self.normalize_email(email),
            usdt_address=usdt_address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, usdt_address, password=None):
        user = self.create_user(
            email,
            password=password,
            usdt_address=usdt_address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    usdt_address = models.CharField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usdt_address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
