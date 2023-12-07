from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Offer , Estate , Address

@admin.register(Estate)
class EstateAdmin(OSMGeoAdmin):
    list_display = ('coordinates',)

admin.site.register(Offer)
admin.site.register(Address)