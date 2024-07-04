from rest_framework import serializers
from .models import *

class ImagePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProperty
        fields = ['id', 'property', 'image']

class PropertySerializer(serializers.ModelSerializer):
    images = ImagePropertySerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'type_operation', 'type_property', 'subtype_property', 'email',
            'first_name', 'last_name', 'dni', 'phone_number', 'adress', 'departamento',
            'provincia', 'distrito', 'urbanization', 'area_property', 'bedrooms_number',
            'garages_number', 'bathrooms_number', 'kitchens_number', 'floors_number',
            'type_currency', 'price', 'description', 'terms_conditions', 'images','user_id'
        ]