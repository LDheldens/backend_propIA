from django.db import models
from users.models import User  # Importa tu modelo User personalizado
import os
import uuid

# Función para generar nombres únicos para las imágenes
def get_unique_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('property/image/', filename)

# Modelo Property
class Property(models.Model):
    # Relación con el modelo User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties',null=True)  # Llave foránea hacia User
    
    type_operation = models.CharField(max_length=20) 
    type_property = models.CharField(max_length=50)
    subtype_property = models.CharField(max_length=50)
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dni = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=9)
    adress = models.CharField(max_length=150)
    departamento = models.CharField(max_length=30)
    provincia = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50)
    urbanization = models.CharField(max_length=30)
    area_property = models.DecimalField(max_digits=10, decimal_places=3)
    bedrooms_number = models.CharField(max_length=2)
    garages_number = models.CharField(max_length=2)
    bathrooms_number = models.CharField(max_length=2)
    kitchens_number = models.CharField(max_length=2)
    floors_number = models.CharField(max_length=2)
    type_currency = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=20, decimal_places=3)
    description = models.TextField(max_length=800)
    terms_conditions = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type_property} - {self.adress}'

# Modelo ImageProperty
class ImageProperty(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_unique_file_path)

    def __str__(self):
        return f'Image for {self.property}'
