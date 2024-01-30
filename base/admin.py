from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *

@admin.register(Estate)
class EstateAdmin(OSMGeoAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(OSMGeoAdmin):
    pass

admin.site.register(Offer)
admin.site.register(Address)
