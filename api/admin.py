from django.contrib import admin
# Register your models here.
from .models import Location, Alert


admin.site.register(Location)
admin.site.register(Alert)