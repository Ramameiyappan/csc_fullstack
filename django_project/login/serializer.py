from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_password(self, value):
        username = self.initial_data.get('username')
        user_obj = User(username=username)
        validate_password(value, user=user_obj)
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['role'] = 'operator'
        validated_data['manager_request'] = False
        return super().create(validated_data)