import django_filters
from .models import Offer , Estate


#----this method needs the exact genre name----#
class EstateFilter(django_filters.FilterSet):
    # estate = django_filters.CharFilter(field_name="space", lookup_expr='icontains')
    # genres = django_filters.ModelMultipleChoiceFilter(field_name="genre__name", to_field_name='name', queryset=Genre.objects.all())
    address = django_filters.ModelMultipleChoiceFilter(field_name="address__city", to_field_name='city',queryset=Estate.objects.all())
    class Meta: 
        model = Estate
        fields = ['address', 'space']