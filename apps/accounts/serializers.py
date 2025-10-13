from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model=UserProfile
        fields=['id','username', 'email', 'first_name', 'last_name', 'currency','income_period','income_amount']
        read_only_fields = ['id','username','email','first_name','last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    passwordValidator = serializers.CharField(write_only=True)
    
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    currency = serializers.CharField(default='USD')
    income_period = serializers.CharField(default='monthly')
    income_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'passwordValidator',
            'first_name',
            'last_name',
            'currency',
            'income_period',
            'income_amount'
        ]
    
    def validate(self, attrs):
        password = attrs['password']
        passwordValidator = attrs['passwordValidator']

        if password != passwordValidator:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('passwordValidator')

        currency = validated_data.pop('currency')
        income_period = validated_data.pop('income_period')
        income_amount = validated_data.pop('income_amount')

        user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
        )

        UserProfile.objects.create(
        user=user,
        currency=currency,
        income_period=income_period,
        income_amount=income_amount
        )

        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_passwordValidator = serializers.CharField(write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Contraseña actual incorrecta")
        return value
    
    def validate(self, attrs):
        new_password = attrs['new_password']
        new_passwordValidator = attrs['new_passwordValidator']
        if not new_password == new_passwordValidator:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs

    
    def save(self):
        user = self.context['request'].user
        password = self.validated_data['new_password']

        user.set_password(password)
        user.save()