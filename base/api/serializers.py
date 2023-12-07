from rest_framework import serializers
from base.models import Offer , Estate
from django.contrib.gis.geos import GEOSGeometry



class EstateSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    class Meta:
        model = Estate
        fields = '__all__'

    def get_distance(self,obj):
        distance =  getattr(obj,'distance',None)
        return distance.m if distance else None
    def get_longitude(self,obj):
        point = GEOSGeometry(obj.coordinates)
        return [point.x,point.y]



class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'