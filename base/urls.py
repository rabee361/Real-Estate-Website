from django.urls import include
from django.urls import path
from .views.views import *
from .views.auth import *

authPatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

urlpatterns = [
    path('' , HomeView.as_view() , name="home"),
    path('offers/<int:estate_id>' , ListOffersPerEstate.as_view() , name="estate_offers"),
    path('estates/' , EstatesView.as_view(), name="estates"),
    path('estates/<int:pk>' , GetEstate.as_view() , name="estate"),
    # path('estates-near/' , EstatesNear.as_view()),
    # path('owner-info/<str:owner_id>/' , OwnerInfo.as_view() , name="owner-info"),
    # path('make-offer/<str:estate_id>/' , MakeOffer.as_view() , name="make-offer"),
    # path('withdraw-offer/<str:estate_id>/' , WithdrawOffer.as_view() , name="withdraw-offer"),
    # path('sign-up/' , SignUpView.as_view() , name="sign-up"),
    # path('login/' , LoginView.as_view() , name="login"),
    # path('logout/' , LogoutView.as_view() , name="logout"),

    # path('home/' , HomeView.as_view()) 
    path('auth/', include(authPatterns))
]

