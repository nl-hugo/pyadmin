from django.contrib import admin

from .models import Location, Trip


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ('name', 'zip_code', 'city', 'lat', 'lon', )
    list_filter = ['city', ]
    search_fields = ['name', 'zip_code', 'city', ]
    readonly_fields = ('city', 'lat', 'lon',)


admin.site.register(Location, LocationAdmin)


class TripAdmin(admin.ModelAdmin):
    model = Trip
    list_display = ('date', 'origin', 'destination', 'description', 'is_return', 'distance', 'allowance', 'api_return_code', )
    list_filter = ['date', 'destination', ]
    search_fields = ['origin', 'destination', 'description', ]
    readonly_fields = ('quarter', 'year', 'distance', 'allowance', 'api_return_code', 'api_message', )


admin.site.register(Trip, TripAdmin)
