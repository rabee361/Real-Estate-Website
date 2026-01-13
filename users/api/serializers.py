from rest_framework import serializers
from base.models import *
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login , authenticate
from django.contrib.gis.geos import Point
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken , TokenError
from rest_framework.response import Response


#----------------------------Authentication---------------------------#

class SignUpSerializer(serializers.ModelSerializer):
    x = serializers.FloatField(write_only=True)
    y = serializers.FloatField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password','password2','x','y']
        extra_kwargs = {
            'password':{'write_only':True,}
        }

    def validate(self, validated_data):
        password = validated_data['password']
        password2 = validated_data.pop('password2')
        validate_password(password)
        if password2 == password:
            return validated_data
        else:
            raise ValueError({"error":"passwords Don't match"})

    def create(self, validated_data):
        x = validated_data.pop('x')
        y = validated_data.pop('y')
        validated_data['location'] = Point(x, y)
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        return user
    



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)
    def validate(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        return validated_data
    



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_representation(self, instance):
        r = super().to_representation(instance)
        return r['username']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phonenumber', 'password', 'image']

