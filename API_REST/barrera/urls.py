from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BarreraViewSet

router = DefaultRouter()
router.register(r'barrera', BarreraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
