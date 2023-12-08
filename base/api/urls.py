from django.urls import path
from .views import *

urlpatterns = [
    path('offers/' , ListOffersPerEstate.as_view() , name="offers"),
    path('estates/' , ListEstates.as_view(), name="estates"),
    path('near-by/' , OffersNear.as_view()),
    path('login/', Login.as_view() , name="login"),
    path('logout/' , Logout.as_view() , name="logout"),
    path('sign-up/' , SignUp2.as_view() , name="sign-up")

]
