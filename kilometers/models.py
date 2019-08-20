import logging

import geopy
from django.core.validators import RegexValidator
from django.db import models

from uren.models import Project, Activity

logger = logging.getLogger(__name__)

validate_zip_code = RegexValidator(r'^\d{4}\s?\w{2}$', 'Invalid zip code.')


def quarter(date):
    return '{}-Q{}'.format(date.year, (date.month - 1) // 3 + 1)


def get_default_location():
    return Location.objects.filter(is_default=True).first()


class Location(models.Model):
    name = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=10, validators=[validate_zip_code])
    city = models.CharField(max_length=100, null=True, blank=True)
    lat = models.CharField(max_length=20, null=True, blank=True)
    lon = models.CharField(max_length=20, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return '{} ({})'.format(self.name, self.zip_code)

    def as_geo_location(self):
        return geopy.location.Location(point=(self.lat, self.lon))

    class Meta:
        ordering = ['name']


class Trip(models.Model):
    date = models.DateField()
    quarter = models.CharField(max_length=8)
    year = models.PositiveSmallIntegerField(default=0)
    origin = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='trip_from',
                               default=get_default_location)
    destination = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='trip_to')
    description = models.CharField(max_length=500, blank=True)
    is_return = models.BooleanField(default=True)
    distance = models.PositiveSmallIntegerField(default=0)
    api_return_code = models.CharField(max_length=3, null=True, blank=True)
    api_message = models.CharField(max_length=500, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='trips', blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT, related_name='trips', blank=True, null=True)

    def __str__(self):
        return '{} to {}'.format(self.origin, self.destination)

    def save(self, *args, **kwargs):
        self.quarter = quarter(self.date)
        self.year = self.date.year
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
