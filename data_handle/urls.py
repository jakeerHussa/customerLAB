from django.urls import path
from.views import incoming_data

urlpatterns = [
    path('server/incoming_data/', incoming_data),
]