from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import (
    HttpResponse, 
    HttpResponseNotAllowed, 
    HttpResponseBadRequest,
    HttpResponseNotFound
)

from django.http.response import JsonResponse
from . serializers import UserSerializer
from django.contrib.auth.models import User



# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed('Not allowed to make the request')
    
    users = User.objects.all()
    usersSerial = UserSerializer(users, many=True)
    return JsonResponse(usersSerial.data, safe=False)

def user(request, userId):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed('Not allowed to make the request')

    if request.method == 'GET':
        if id is None:
            return HttpResponseBadRequest('Params cannot be null/none')

        try:
            user = User.objects.get(pk=userId)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('User not found')

        userSerial = UserSerializer(user)
        return JsonResponse(userSerial.data, safe=False)
    
    if request.method == 'DELETE':
        pass
    
    if request.method == 'PUT':
        pass
        
    return HttpResponseNotFound()