import django_filters

from kilometers.models import Trip


class TripFilter(django_filters.FilterSet):
    year = django_filters.filters.AllValuesFilter(label='Jaar')

    class Meta:
        model = Trip
        fields = ['year', ]
