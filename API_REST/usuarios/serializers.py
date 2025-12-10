from rest_framework import serializers
from .models import Usuario, Departamento
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import re

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

    def validate_nombre(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El nombre del departamento debe tener al menos 3 caracteres."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "El nombre del departamento no puede exceder 100 caracteres."
            )
        return value.strip().title()
    
    def validate_zona(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "La zona debe tener al menos 3 caracteres."
            )
        return value.strip()
    
    def validate(self, attrs):
        nombre = attrs.get('nombre')
        zona = attrs.get('zona')
        
        if self.instance:
            if Departamento.objects.exclude(pk=self.instance.pk).filter(
                nombre=nombre, zona=zona
            ).exists():
                raise serializers.ValidationError(
                    f"Ya existe un departamento '{nombre}' en la zona '{zona}'."
                )
        else:
            if Departamento.objects.filter(nombre=nombre, zona=zona).exists():
                raise serializers.ValidationError(
                    f"Ya existe un departamento '{nombre}' en la zona '{zona}'."
                )
        
        return attrs

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

    def validate_username(self, value):
        """Validar username"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El nombre de usuario debe tener al menos 3 caracteres."
            )
        
        # Solo letras, números y guiones bajos
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "El nombre de usuario solo puede contener letras, números y guiones bajos."
            )
        
        # Validar que no exista (excepto en actualización)
        if self.instance:
            if User.objects.exclude(pk=self.instance.user.pk).filter(username=value).exists():
                raise serializers.ValidationError(
                    f"El nombre de usuario '{value}' ya está en uso."
                )
        else:
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError(
                    f"El nombre de usuario '{value}' ya está en uso."
                )
        
        return value.lower()
    
    def validate_email(self, value):
        """Validar email"""
        if not value:
            raise serializers.ValidationError("El email es obligatorio.")
        
        # Validar formato básico
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Formato de email inválido.")
        
        # Validar que no exista (excepto en actualización)
        if self.instance:
            if User.objects.exclude(pk=self.instance.user.pk).filter(email=value).exists():
                raise serializers.ValidationError(
                    f"El email '{value}' ya está registrado."
                )
        else:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    f"El email '{value}' ya está registrado."
                )
        
        return value.lower()
    
    def validate_password(self, value):
        """Validar contraseña segura"""
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        
        # Al menos una letra mayúscula
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula."
            )
        
        # Al menos una letra minúscula
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra minúscula."
            )
        
        # Al menos un número
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un número."
            )
        
        return value
    
    def validate_rol(self, value):
        """Validar que el rol sea válido"""
        roles_validos = ['admin', 'operador']
        if value.lower() not in roles_validos:
            raise serializers.ValidationError(
                f"Rol inválido. Debe ser uno de: {', '.join(roles_validos)}"
            )
        return value.lower()
    
    def validate_departamento(self, value):
        """Validar que el departamento existe"""
        try:
            Departamento.objects.get(id=value)
        except Departamento.DoesNotExist:
            raise serializers.ValidationError(
                f"El departamento con ID {value} no existe."
            )
        return value

    def create(self, validated_data):
        try:
            departamento = Departamento.objects.get(id=validated_data['departamento'])
        except Departamento.DoesNotExist:
            raise serializers.ValidationError("Departamento no encontrado")
        
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
        # Actualizar User
        instance.user.username = validated_data.get('username', instance.user.username)
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        if 'password' in validated_data:
            instance.user.set_password(validated_data['password'])
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