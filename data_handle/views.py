from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from account.models import Account
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes((AllowAny,))
def incoming_data(request):
    app_secret_token = request.headers.get('CL-X-TOKEN')
    print(app_secret_token)
    if not app_secret_token:
        return JsonResponse({'error': 'Un Authenticate'}, status=401)
    account = Account.objects.get(app_secret_token=app_secret_token)
    data = request.POST
    if not data or not isinstance(data, dict):
        return JsonResponse({'error': 'Invalid Data'}, status=400)
    for destination in account.destination_set.all():
        print(destination)
        headers = destination.headers
        if destination.http_method == 'GET':
            params = data
        else:
            params = None
        response = requests.request(destination.http_method, destination.url, headers=headers, json=data, params=params)
        if response.status_code!= 200:
            return JsonResponse({'error': 'Error sending data to destination'}, status=500)
    return JsonResponse({'message': 'Data sent successfully'}, status=200)