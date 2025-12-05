"""
URL configuration for API_REST project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from auditoria.urls import urlpatterns as auditoria_urls
from sensores.urls import urlpatterns as sensores_urls
from barrera.urls import urlpatterns as barrera_urls
from usuarios.urls import urlpatterns as usuarios_urls
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(auditoria_urls)),
    path('api/', include(sensores_urls)),
    path('api/', include(barrera_urls)),
    path('api/', include(usuarios_urls)),
    path('api-token/', obtain_auth_token),
]
