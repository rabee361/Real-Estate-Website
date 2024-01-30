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
    










# class SignUpSerializer(serializers.ModelSerializer):
#     x = serializers.FloatField(write_only=True)
#     y = serializers.FloatField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'username', 'password','x','y']
#         extra_kwargs = {
#             'password':{'write_only':True,}
#         }

#     def validate(self, validated_data):
#         validate_password(validated_data['password'])
#         return validated_data

#     def create(self, validated_data):
#         x = validated_data.pop('x')
#         y = validated_data.pop('y') 
#         password = validated_data.pop('password')
#         validated_data['location'] = Point(x, y)
#         hashed = make_password(password)
#         return CustomUser.objects.create_user(password=hashed,**validated_data)



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




class OfferSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    class Meta:
        model = Offer
        fields = '__all__'

    def to_representation(self, instance):
        r = super().to_representation(instance)
        return r['user']
    


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def to_representation(self, instance):
        return f'{instance.country}/{instance.governate}/{instance.area}/{instance.neighborhood}/{instance.building_no}'


class EstateSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False,read_only=True)
    distance = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    offers = OfferSerializer(many=True,read_only=True)
    address = AddressSerializer(many=False,read_only=True)
    class Meta:
        model = Estate
        fields = '__all__'

    def get_distance(self,obj):
        distance =  getattr(obj,'distance',None)
        return f'{int(distance.m)} m' if distance else None
    def get_coordinates(self,obj):
        point = GEOSGeometry(obj.coordinates)
        return [point.x,point.y]



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            return serializers.ValidationError("passwords don't match")
        validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        login(request,user)
        return user
