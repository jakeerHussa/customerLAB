from django.urls import path
from .views import get_accounts, create_account, get_destinations, create_destination,update_account,delete_account,update_destination,delete_destination

urlpatterns = [
    path('get_accounts', get_accounts),
    path('create_account', create_account),
    path('update_account',update_account),
    path('delete_account',delete_account),
    
    path('get_destinations', get_destinations),
    path('create_destination', create_destination),    
    path('update_destination',update_destination),
    path('delete_destination',delete_destination),
]