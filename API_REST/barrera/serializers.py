from rest_framework import serializers
from .models import Barrera

class BarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrera
        fields = '__all__'