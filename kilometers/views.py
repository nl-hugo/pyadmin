from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render

from kilometers.filters import TripFilter
from kilometers.models import Trip


def search_trips(request):
    trip_list = Trip.objects.all()
    trip_filter = TripFilter(request.GET, queryset=trip_list)

    # Paginate results to show n items per page
    paginator = Paginator(trip_filter.qs.order_by('-date'), 10)
    page = request.GET.get('page')
    trips = paginator.get_page(page)

    # Provide totals
    totals = trip_filter.qs.aggregate(distance=Coalesce(Sum('distance'), 0), )

    # Aggregate by destination
    destinations = trip_filter.qs.values('destination__name',
                                         'destination__lat', 'destination__lon').annotate(
        count=Count(1)).order_by('-count')  # won't work without the order_by!

    # Aggregate by quarter
    quarterly = trip_filter.qs.values('quarter').annotate(distance=Sum('distance')).order_by('-quarter')

    return render(request, 'kilometers/trips.html', {
        'trips': trips,
        'destinations': list(destinations),
        'quarterly': quarterly,
        'form': trip_filter.form,
        'total_distance': totals.get('distance'),
    })
