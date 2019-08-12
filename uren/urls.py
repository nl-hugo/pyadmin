from django.contrib.auth.decorators import login_required
from django.urls import path

from uren import views

# Create a router and register our viewsets with it.
app_name = 'uren'

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    # path('', login_required(views.list_uren), name='index'),
    path('', login_required(views.UrenListView.as_view()), name='index'),
]
