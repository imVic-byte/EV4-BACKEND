from rest_framework import serializers
from .models import Usuario, Departamento
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

    def create(self, validated_data):
        if Departamento.objects.filter(nombre=validated_data['nombre'], zona=validated_data['zona']).exists():
            raise serializers.ValidationError("Departamento ya existe")
        departamento = Departamento.objects.create(**validated_data)
        return departamento

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "rol", "departamento", "username", "email", "password", "first_name", "last_name"
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    rol = serializers.CharField(max_length=10)
    departamento = serializers.CharField(max_length=100) 

    def create(self, validated_data):
        try:
            departamento = Departamento.objects.get(id=validated_data['departamento'])
        except Departamento.DoesNotExist:
            raise serializers.ValidationError("Departamento no encontrado")
        if User.objects.filter(username=validated_data.get('username')).exists():
            raise serializers.ValidationError("Usuario ya existe")
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError("Email ya registrado")
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
        }
        profile_data = validated_data 
        user = User.objects.create_user(**user_data)
        usuario = Usuario.objects.create(
            user=user, 
            rol=profile_data['rol'],
            departamento=departamento
        )
        return usuario
    
    def to_representation(self, instance):
        user = instance.user
        token, created = Token.objects.get_or_create(user=user)
        usuario = instance
        return {
            'id': instance.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'rol': instance.rol,
            'departamento': instance.departamento.id,
            'token': token.key
        }


    def update(self, instance, validated_data):
        instance.user.username = validated_data.get('username', instance.user.username)
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        instance.user.save()
        instance.rol = validated_data.get('rol', instance.rol)
        if validated_data.get('departamento'):
            departamento = Departamento.objects.get(id=validated_data.get('departamento'))
            instance.departamento = departamento
        instance.save()
        return instance

    def delete(self, instance):
        instance.user.delete()
        instance.delete()

#NECESARIO PQ HAY QUE CREAR EL PRIMER USUARIO SIN AUTENTICACION
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    rol = serializers.CharField(max_length=10)
    departamento = serializers.CharField(max_length=100) 

    def create(self, validated_data):
        if User.objects.exists():
            raise serializers.ValidationError("Ya existen usuarios en la DB, no se puede usar este método.")
        try:
            departamento = Departamento.objects.get(id=validated_data['departamento'])
        except Departamento.DoesNotExist:
            raise serializers.ValidationError("Departamento no encontrado")
        if User.objects.filter(username=validated_data.get('username')).exists():
            raise serializers.ValidationError("Usuario ya existe")
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError("Email ya registrado")
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
        }
        profile_data = validated_data 
        user = User.objects.create_user(**user_data)
        usuario = Usuario.objects.create(
            user=user, 
            rol=profile_data['rol'],
            departamento=departamento
        )
        return usuario
    
    def to_representation(self, instance):
        user = instance.user
        token, created = Token.objects.get_or_create(user=user)
        usuario = instance
        return {
            'id': instance.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'rol': instance.rol,
            'departamento': instance.departamento.id,
            'token': token.key
        }

#NECESARIO PQ HAY QUE CREAR EL PRIMER DEPARTAMENTO SIN AUTENTICACION
class DepartamentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'
    
    def create(self, validated_data):
        if User.objects.exists():
            raise serializers.ValidationError("Ya existen usuarios en la DB, no se puede usar este método.")
        departamento = Departamento.objects.create(**validated_data)
        return departamento