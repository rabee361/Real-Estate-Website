import django_filters
from .models import Offer , Estate

    
#----this method needs the exact genre name----#
class EstateFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(field_name="address__area", lookup_expr='icontains')
    price = django_filters.CharFilter(field_name='price' , lookup_expr='lte')
    space = django_filters.CharFilter(field_name='space' , lookup_expr='lte')
    class Meta: 
        model = Estate
        fields = ['address', 'space','price']