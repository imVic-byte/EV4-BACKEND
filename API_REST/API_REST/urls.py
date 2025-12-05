from django.contrib import admin
from django.urls import path, include
from auditoria.urls import urlpatterns as auditoria_urls
from sensores.urls import urlpatterns as sensores_urls
from barrera.urls import urlpatterns as barrera_urls
from usuarios.urls import urlpatterns as usuarios_urls
from info.urls import urlpatterns as info_urls
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(auditoria_urls)),
    path('api/', include(sensores_urls)),
    path('api/', include(barrera_urls)),
    path('api/', include(usuarios_urls)),
    path('api/', include(info_urls)),
    path('api-token/', obtain_auth_token),
]
