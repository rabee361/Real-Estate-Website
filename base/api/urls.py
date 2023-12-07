from django.urls import path
from .views import *

urlpatterns = [
    path('offers/' , ListOffersPerEstate.as_view() , name="offers"),
    path('estates/' , ListEstates.as_view(), name="estates"),
    path('near-by/' , OffersNear.as_view())

]
