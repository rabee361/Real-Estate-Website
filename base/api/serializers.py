from rest_framework import serializers
from base.models import Offer , Estate ,Address
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        r = super().to_representation(instance)
        return r['username']



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



