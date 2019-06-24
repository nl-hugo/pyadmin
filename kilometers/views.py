from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator

# from rest_framework import authentication, permissions
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes

from kilometers.geocoders import geoCode, getDrivingDistance
from kilometers.models import Trip
from kilometers.filters import TripFilter


def searchTrips(request):
    trip_list = Trip.objects.all()
    trip_filter = TripFilter(request.GET, queryset=trip_list)

    # Paginate results to show n items per page
    paginator = Paginator(trip_filter.qs.order_by('-date'), 10)
    page = request.GET.get('page')
    trips = paginator.get_page(page)

    # Provide totals
    totals = trip_filter.qs.aggregate(distance=Coalesce(Sum('distance'), 0),
        allowance=Coalesce(Sum('allowance'), 0),)

    # Aggregate by destination
    destinations = trip_filter.qs.values('destination__name',
        'destination__lat', 'destination__lon').annotate(
        count=Count(1)).order_by('-count') # won't work without the order_by!

    # Aggregate by quarter
    quarterly = trip_filter.qs.values('quarter').annotate(
        distance=Sum('distance'),
        allowance=Sum('allowance')).order_by('-quarter')

    return render(request, 'kilometers/trips.html', {
        'trips': trips,
        'destinations': list(destinations),
        'quarterly': quarterly,
        'form': trip_filter.form,
        'total_distance': totals.get('distance'),
        'total_allowance': totals.get('allowance'),
    })


# @api_view()
# @permission_classes((permissions.AllowAny,))
# # @authentication_classes(...)
# # @permission_classes(...)
# def hello_world(request, origin='', destination=''):
#     print(request.method)
#     # print(request.data)
#     print(origin)
#     print(destination)
#     # print(args)
#     # print(request.data.get('args', ''))
#     loc_from = geoCode(origin)
#     loc_to = geoCode(destination)
#     distance = getDrivingDistance(loc_from, loc_to)

#     return Response({"message": "Hello, world! {} - {} - {} km".format(origin, destination, distance)})
# # http://localhost:8000/distance/3512JC/3584AA/?format=json
