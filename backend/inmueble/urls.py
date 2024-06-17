from django.urls import path
from .views import *
#El atributo app_name te permite especificar un nombre de aplicación para todas las URL definidas en ese archivo
app_name = 'inmueble'

urlpatterns = [
    path('list/',ListProperty),
    path('detail/<int:pk>/',DetailProperty),
    path('create/',CreateProperty),
    path('update/<int:pk>/',UpdateProperty),
    path('delete/<int:pk>/',DeleteProperty),
]
