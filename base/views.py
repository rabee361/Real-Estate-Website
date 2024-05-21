from rest_framework.response import Response
from base.models import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , RetrieveAPIView , CreateAPIView
from .serializers import *
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from base.filters import EstateFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
# from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.gis.measure import D
from rest_framework.permissions import IsAuthenticated



# class SignupView(APIView):
#     def post(self, request, *args, **kwargs):
#         form = SignupForm(request.data)
#         if form.is_valid():
#             user = form.save(request)
#             get_adapter().save_user(request, user, form)
#             complete_signup(request, user, None, None)
#             return Response({"detail": "Successfully signed up."}, status=status.HTTP_200_OK)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)




class HomeView(APIView):
    def get(self,request):
        return Response(
            {"welcome home !!!"}
        )
    




# class test(APIView):
#     def get(self,request):
#         file = "12.pdf"
#         images = convert_pdf_to_images(file)
#         paginator = Paginator(images, 10)
#         page_number = request.GET.get('page', 1)
#         page = paginator.get_page(page_number)
#         page_dict = {
#             'count': paginator.count,
#             'num_pages': paginator.num_pages,
#             'current_page': page.number,
#             'next_page': page.has_next(),
#             'previous_page': page.has_previous(),
#             'results': [item for item in page],
#         }
#         return Response(page_dict)



#------------------ Authentication ----------------------------#
    


class SignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class  = SignUpSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        tokens = {
            'refresh':str(token),
            'accsess':str(token.access_token)
        }
        return Response({'username':user.username,
                         'email':user.email,
                         'tokens':tokens})





class LoginView(APIView):
    def post(self, request, *args, **kwargs):  
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(username = request.data['username']).first()
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)



class LogoutView(APIView):
    serializer_class = LogoutSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)






class ListEstates(ListAPIView):
    queryset = Estate.objects.defer('offers').select_related('owner').all()
    serializer_class = EstateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstateFilter


class ListOffersPerEstate(RetrieveAPIView):
    queryset = Estate.objects.all()
    serializer_class = OfferSerializer


class GetEstate(RetrieveAPIView):
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer


class EstatesNear(ListAPIView):
    queryset = Estate.objects.all()
    serializer_class = EstateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pnt = user.location
        if pnt:
            estates = Estate.objects.annotate(distance=Distance('coordinates', pnt))\
                                    .filter(distance__lte=D(km=100))\
                                    .order_by('distance')
        else:
            estates = Estate.objects.all()

        return estates



