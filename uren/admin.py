from django.contrib import admin

from .models import Client, Project, ProjectHours


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('name', )
    # list_filter = ['city', ]
    # search_fields = ['name', 'zip_code', 'city', ]
    # readonly_fields = ('city', 'lat', 'lon',)


admin.site.register(Client, ClientAdmin)


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('name', )
    # list_filter = ['city', ]
    # search_fields = ['name', 'zip_code', 'city', ]
    # readonly_fields = ('city', 'lat', 'lon',)


admin.site.register(Project, ProjectAdmin)


class ProjectHoursAdmin(admin.ModelAdmin):
    model = ProjectHours
    list_display = ('date', 'project', 'hours', )
    # list_filter = ['city', ]
    # search_fields = ['name', 'zip_code', 'city', ]
    # readonly_fields = ('city', 'lat', 'lon',)


admin.site.register(ProjectHours, ProjectHoursAdmin)
