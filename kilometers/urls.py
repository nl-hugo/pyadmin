from django.conf.urls import include, url, re_path
from django.contrib.auth.decorators import login_required
from django.urls import path
from rest_framework.routers import DefaultRouter
from kilometers import views

# Create a router and register our viewsets with it.
app_name = 'kilometers'

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('', login_required(views.searchTrips), name='index'),
    # re_path(r'^distance/(?P<origin>\d{4}[A-Z]{2})/(?P<destination>\d{4}[A-Z]{2})/$', views.hello_world),
]
