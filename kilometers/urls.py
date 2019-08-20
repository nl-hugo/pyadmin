from django.contrib.auth.decorators import login_required
from django.urls import path

from kilometers import views

# Create a router and register our viewsets with it.
app_name = 'kilometers'

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('', login_required(views.search_trips), name='index'),
]
