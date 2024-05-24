from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes((AllowAny,))
def get_accounts(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes((AllowAny,))
def create_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        account_id = request.POST.get('account_id')
        account_name = request.POST.get('account_name')
        website = request.POST.get('website')
        account = Account(email=email, account_id=account_id, account_name=account_name, website=website)
        account.save()
        return JsonResponse({'message': 'Account created successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_account(request):
    if request.method == 'PUT':
        if 'token' in request.data:
            token = request.data['token']
            try:
                account = Account.objects.get(app_secret_token=token)
            except:
                account = None
        if account is not None:
            if 'email' in request.data:
                account.email = request.data['email']
            if 'account_id' in request.data:
                account.account_id = request.data['account_id']
            if 'website' in request.data:
                account.website = request.data['website']
            if 'account_name' in request.data:
                account.account_name = request.data['account_name']
            account.save() 
            return JsonResponse({'message': 'Account has been updated successfully'}, status=200)
        else:
            return JsonResponse({'error':'token has not foun'},status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_account(request):
    token = request.data.get('token')
    if not token:
        return JsonResponse({"error": "Token is missing in the request data."}, status=400)
    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return JsonResponse({"msg": "Account not found."}, status=404)
    try:
        destinations = Destination.objects.filter(account=account)
        for destination in destinations:
            destination.delete()
        account.delete()
    except Exception as e:
        return JsonResponse({"error": "An error occurred while deleting the data."}, status=500)
    return JsonResponse({"msg": "Data deleted successfully."}, status=200)
        


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_destinations(request):
    account_id = request.data['account_id'] 
    destinations = Destination.objects.filter(account_id=account_id)
    values = DestinationSerializer(destinations,many=True)
    return JsonResponse(values.data,safe=False) 

@api_view(['POST'])
@permission_classes((AllowAny,))
def create_destination(request):
    if request.method == 'POST':
        account_id = request.data['account_id']
        account = Account.objects.get(pk=account_id) 
        url = request.data['url']
        http_method = request.data['http_method']
        headers = request.data['headers']
        destination = Destination(account=account, url=url, http_method=http_method, headers=headers)
        destination.save()
        return JsonResponse({'message': 'Destination created successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_destination(request):
    if request.method == 'PUT':
        destination_id = request.data['destination_id']
        try:
            destination = Destination.objects.get(pk=destination_id) 
        except:
            return JsonResponse({"message":'Destination is not fount'})
        if 'url' in request.data:
            destination.url = request.data['url']
        if 'http_method' in request.data:
            destination.http_method = request.data['http_method']
        if 'headers' in request.data:
            destination.headers = request.data['headers']
        if 'account_id' in request.data:
            destination.account = request.data['account_id']
        destination.save()
        return JsonResponse({'message': 'Destination Updated successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_destination(request):
    if request.method == 'DELETE':
        destination_id = request.data['destination_id']
        try:
            destination = Destination.objects.get(pk=destination_id) 
        except:
            return JsonResponse({"message":'Destination is not fount'})
        if destination is not None:
            destination.delete()
            return JsonResponse({'message': 'Destination deleted successfully'}, status=200)
        else:
            return JsonResponse({"message":"destination is not found"},status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)