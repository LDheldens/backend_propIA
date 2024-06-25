from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,default=2)
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, blank=True, null=True)
    phone = models.IntegerField(null=True, blank=True)

    # Define el campo 'email' como el campo de autenticación.
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'

    # Define los campos adicionales requeridos al crear un usuario.
    REQUIRED_FIELDS = ['first_name', 'last_name','password']
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
