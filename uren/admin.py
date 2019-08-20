from django.contrib import admin

from .models import Client, Project, ProjectHours, Unit, Activity


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [ProjectInline, ]
    list_display = ('name',)


admin.site.register(Client, ClientAdmin)


class ProjectHoursAdmin(admin.ModelAdmin):
    model = ProjectHours
    list_display = ('date', 'project', 'activity', 'hours',)


admin.site.register(ProjectHours, ProjectHoursAdmin)
admin.site.register(Unit)


class ActivityAdmin(admin.ModelAdmin):
    model = Activity
    list_display = ('code', 'description', 'is_billable', 'unit', 'price', 'vat',)


admin.site.register(Activity, ActivityAdmin)
