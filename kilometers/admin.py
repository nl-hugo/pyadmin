from django.contrib import admin

from .models import Location, Trip


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ('name', 'zip_code', 'city', 'lat', 'lon',)
    list_filter = ['city', ]
    search_fields = ['name', 'zip_code', 'city', ]
    readonly_fields = ('city', 'lat', 'lon',)


admin.site.register(Location, LocationAdmin)


class TripAdmin(admin.ModelAdmin):
    model = Trip
    list_display = (
        'date', 'origin', 'destination', 'description', 'get_project_name', 'is_billable', 'is_return', 'distance',
        'api_return_code',)
    list_filter = ['date', 'destination', ]
    search_fields = ['origin', 'destination', 'description', ]
    readonly_fields = ('quarter', 'year', 'distance', 'api_return_code', 'api_message',)

    def get_project_name(self, obj):
        return obj.project.name if obj.project else ''

    get_project_name.admin_order_field = 'project'
    get_project_name.short_description = 'Project'

    def is_billable(self, obj):
        return obj.activity.is_billable if obj.activity else False

    is_billable.admin_order_field = 'activity__is_billable'
    is_billable.boolean = True
    is_billable.short_description = 'Billable'


admin.site.register(Trip, TripAdmin)
