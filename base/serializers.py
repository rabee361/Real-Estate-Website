from rest_framework import serializers
from base.models import *
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login
from users.api.serializers import *



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
