from django.urls import path
from .views import *

app_name = 'contact'

urlpatterns = [
    path('create/',create_message),
    path('list/',list_messages),
    path('detail/',detail_message),
    path('delete/',delete_message),
]
