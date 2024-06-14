from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,null=True)
    photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, blank=True, null=True)
    phone = models.IntegerField(default=1)

    # Define el campo 'email' como el campo de autenticación.
    email = models.EmailField(unique=True, default="defaultemalin@gmail.com")
    USERNAME_FIELD = 'email'

    # Define los campos adicionales requeridos al crear un usuario.
    REQUIRED_FIELDS = ['username','role', 'first_name', 'last_name', 'phone']
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
