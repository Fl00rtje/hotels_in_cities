from django.contrib import admin
from .models import City, Hotel


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_filter = ['name']
    search_fields = ['name', 'code']


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ['name']


admin.site.register(City, CityAdmin)
admin.site.register(Hotel, HotelAdmin)


