from rest_framework.response import Response
from base.models import Offer , Estate
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , RetrieveAPIView , CreateAPIView
from .serializers import EstateSerializer , OfferSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from base.filters import EstateFilter
from django_filters.rest_framework import DjangoFilterBackend


class ListEstates(ListAPIView):
    queryset = Estate.objects.defer('offers').select_related('owner').all()
    serializer_class = EstateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstateFilter


class ListOffersPerEstate(RetrieveAPIView):
    queryset = Estate.objects.all()
    serializer_class = OfferSerializer



# class OffersNear(APIView):
#     def get(self,request):
#         pnt = Estate.objects.get(id=1)
#         nearby_estates = Estate.objects.annotate(distance=Distance('longitude', pnt.longitude)).order_by('distance').filter(distance__lte=2000)
#         serializer = EstateSerializer(nearby_estates,many=True)
#         return Response(serializer.data)


class OffersNear(ListAPIView):
    serializer_class = EstateSerializer
    def get_queryset(self):
        longitude = self.request.query_params.get('longitude',None)
        latitude = self.request.query_params.get('latitude',None)
        ptn = Point(float(longitude), float(latitude), srid=4326)

        if ptn:
            estates = Estate.objects.annotate(distance=Distance('coordinates', ptn))\
                                    .order_by('distance').all()
                                        # filter(distance__lte=2000)
        else:
            estates = Estate.objects.all()

        return estates

        