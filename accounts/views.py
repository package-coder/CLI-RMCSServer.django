from django.contrib.auth.models import User
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth import (
    logout, 
    authenticate, 
    login
)
from django.http import (
    HttpResponse, 
    HttpResponseNotAllowed, 
    HttpResponseBadRequest
)

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.middleware import csrf
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET', 'POST'])
def accountLogin(request):

    if request.method=='POST':
        if request.data is not None:

            try:
                username = request.data['username']
                password = request.data['password']
            except KeyError:
                return Response({
                    'error-message': "Key params is not supplied"
                }, status=status.HTTP_403_FORBIDDEN)
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(UserSerializer(user).data)
            else:
                try:
                    User.objects.get(username=username)
                
                except User.DoesNotExist:
                    return Response({
                        'error-message': "This user does not exist"
                    }, status=status.HTTP_404_NOT_FOUND)
                
                else:
                    return Response({
                        'error-message': "Authentication credentials failed"
                    }, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method=='GET' and request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])    
def accountLogout(request):
    if not request.user.is_authenticated:
        return Response({
            'error-message': 'No current use is logged in'
        }, status=status.HTTP_404_NOT_FOUND)

    logout(request)
    return Response({
        'message': 'Logout successfully'
    })

def account(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed('Not allowed to make the request')

    serializer = UserSerializer(User.objects.get(pk=request.user.id))
    return JsonResponse(serializer.data, safe=False)

def cookies(request):
    user = authenticate(username='admin-chris', password='@rmcs.password?101')
    print (request.COOKIES)
    login(request, user)
    
    return HttpResponse(csrf.get_token(request))