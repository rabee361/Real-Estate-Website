from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import *

@admin.register(Estate)
class EstateAdmin(LeafletGeoAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(LeafletGeoAdmin):
    pass

admin.site.register(Offer)
admin.site.register(Address)
admin.site.register(Section)
admin.site.register(SectionEstate)
admin.site.register(Slide)
