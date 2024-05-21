from django.urls import path
from .views import *

urlpatterns = [
    path('offers/' , ListOffersPerEstate.as_view() , name="offers"),
    path('estates/' , ListEstates.as_view(), name="estates"),
    path('near-by/' , EstatesNear.as_view()),
    path('estate/<str:pk>' , GetEstate.as_view() , name="estate"),
    path('user/' , getuser , name="user"),
    # path('login/' , GoogleLoginView.as_view()),
    # path('signup/' , GoogleSignupView.as_view()),
    path('sign-up/' , SignUpView.as_view() , name="sign-up"),
    path('login/' , LoginView.as_view() , name="login"),
    path('logout/' , LogoutView.as_view() , name="logout"),

    path('home/' , HomeView.as_view()) 
]
