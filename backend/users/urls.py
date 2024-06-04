from django.urls import path
from .views import *

#El atributo app_name te permite especificar un nombre de aplicación para todas las URL definidas en ese archivo
app_name = 'auth'

urlpatterns = [
    path('login/',login),
    path('register/',register),
    path('profile/',profile),
]
