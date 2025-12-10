from django.contrib import admin
from django.urls import path, include
from auditoria.urls import urlpatterns as auditoria_urls
from sensores.urls import urlpatterns as sensores_urls
from barrera.urls import urlpatterns as barrera_urls
from usuarios.urls import urlpatterns as usuarios_urls
from info.urls import urlpatterns as info_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .handlers import handler404, handler400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(auditoria_urls)),
    path('api/', include(sensores_urls)),
    path('api/', include(barrera_urls)),
    path('api/', include(usuarios_urls)),
    path('api/info/', include(info_urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

handler404 = 'API_REST.handlers.handler404'
handler400 = 'API_REST.handlers.handler400'