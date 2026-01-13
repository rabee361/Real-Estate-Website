from django.urls import path
from .views import *

urlpatterns = [
    path('offers/' , ListOffersPerEstate.as_view() , name="offers"),
    path('list-estates/' , ListEstates.as_view(), name="list-estates"),
    path('estates-near/' , EstatesNear.as_view()),
    path('get-estate/<str:pk>' , GetEstate.as_view() , name="get-estate"),
    # path('owner-info/<str:owner_id>/' , OwnerInfo.as_view() , name="owner-info"),
    # path('make-offer/<str:estate_id>/' , MakeOffer.as_view() , name="make-offer"),
    # path('withdraw-offer/<str:estate_id>/' , WithdrawOffer.as_view() , name="withdraw-offer"),
    path('sign-up/' , SignUpView.as_view() , name="sign-up"),
    path('login/' , LoginView.as_view() , name="login"),
    path('logout/' , LogoutView.as_view() , name="logout"),

    path('home/' , HomeView.as_view()) 
]
