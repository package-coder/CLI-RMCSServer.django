from django.shortcuts import (
    render,
    get_object_or_404
)

from django.contrib.auth import (
    logout, 
    authenticate,
    login
)
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import UserSerializer


@api_view(['GET'])    
def accountLogout(request):
    if not request.user.is_authenticated:
        return Response({
            'error': "No user found"
        }, status=status.HTTP_404_NOT_FOUND)

    logout(request)
    return Response({
        'message': 'Logout successfully'
    })

class AccountLoginAPI(APIView):
    def get(self, request, format=None):
        if request.user.is_anonymous:
            return Response({
            "error": "No user found"
            },status=status.HTTP_404_NOT_FOUND)

        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        

    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return Response(UserSerializer(user).data)
            else:
                try:
                    User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response({
                        'error': "This user does not exist"
                    }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        'error': "Authentication credentials failed"
                    }, status=status.HTTP_400_BAD_REQUEST)
            