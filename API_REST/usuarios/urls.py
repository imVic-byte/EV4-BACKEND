from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartamentoViewSet, UsuarioViewSet, DepartamentoCreateApiView, UserCreateApiView

router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('usuarios/', include(router.urls)),
    path('create-user/', UserCreateApiView.as_view(), name='user-create'),
    path('create-departamento/', DepartamentoCreateApiView.as_view(), name='departamento-create'),
]