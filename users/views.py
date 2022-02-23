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
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


# Create your views here.
@api_view(['GET'])
def index(request):
    if not request.user.is_authenticated:
        return Response({
            'error-message': 'User is not authenticated' 
        }, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.all()
    usersSerial = UserSerializer(users, many=True)
    return Response(usersSerial.data)

@api_view(['GET', 'DELETE', 'PUT'])
def user(request, userId):
    if not request.user.is_authenticated:
        return Response({
            'error-message': 'User is not authenticated' 
        }, status=status.HTTP_403_FORBIDDEN)


    if request.method == 'GET':
        if userId is None:
            return Response({
                'error-message': 'User is not authenticated' 
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=userId)
        except ObjectDoesNotExist:
            return Response({
                'error-message': 'userId does not exist' 
            }, status=status.HTTP_404_NOT_FOUND)
            
        userSerial = UserSerializer(user)
        return JsonResponse(userSerial.data, safe=False)

    
    if request.method == 'DELETE':
        pass
    
    if request.method == 'PUT':
        pass