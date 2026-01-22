from base.models import Offer, Estate
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'base/home.html'

class EstatesView(View):
    def get(self, request):
        estates = Estate.objects.all()
        return render(request, 'estates/estates.html', {'estates': estates})

class ListOffersPerEstate(View):
    def get(self, request, estate_id):
        offers = Offer.objects.filter(estate_id=estate_id)
        return render(request, 'estates/offers.html', {'estate_offers': offers})
    
class GetEstate(View):
    def get(self, request, estate_id):
        estate = Estate.objects.get(id=estate_id)
        return render(request, 'estates/estate.html', {'estate': estate})