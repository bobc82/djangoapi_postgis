from django.contrib.gis import admin
from .models import NycNeighborhood

# Register your models here.
admin.site.register(NycNeighborhood, admin.GISModelAdmin)
