from rest_framework.response import Response
from base.models import Offer , Estate
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , RetrieveAPIView , CreateAPIView
from .serializers import EstateSerializer , OfferSerializer , UserSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from base.filters import EstateFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import logout,login,authenticate
from rest_framework import status
from django.shortcuts import redirect


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


class SignUp2(CreateAPIView):
    serializer_class = UserSerializer



#-----login-----#
class Login(APIView):
    def get(self,request):
        return Response('hello , you can login here')
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username , password=password)
        if user:
            login(request,user)
            return redirect('books')
        return Response('error' , status=status.HTTP_404_NOT_FOUND)


#----logout----#
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        logout(request)
        return Response('done')

