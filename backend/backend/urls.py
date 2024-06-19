from django.contrib import admin
from django.urls import path, include
from users import urls as usersUrls
from inmueble import urls as inmuebleUrls
from contact import urls as contactUrls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include(usersUrls)),
    path('api/property/',include(inmuebleUrls)),
    path('api/contact/', include(contactUrls))
]
