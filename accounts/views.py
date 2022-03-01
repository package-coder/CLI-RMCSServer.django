import re
from django.http import HttpResponseBadRequest
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
from users.models import User
from django.http.response import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)
from rest_framework.authentication import (
    SessionAuthentication, 
    BasicAuthentication
)
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny
)

from users.serializers import UserSerializer


def logout_user(token):
    token = Token.objects.get(pk=token)
    token.delete()

@api_view()
@permission_classes([IsAuthenticated])
def logout_account(request):
    logout(request)
    print(request.auth)
    token = Token.objects.get(pk=request.auth)
    token.delete()
    return Response({
        'message': 'Logout successfully'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_account(request, format=None):

    username = request.data['username']
    password = request.data['password']

    user = authenticate(username=username, password=password)

    if user is None:
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

    token = None
    if Token.objects.filter(user_id=user.id).exists():
        token = Token.objects.get(user=user)
        token.delete()

    token = Token.objects.create(user=user)
    
    login(request, user)
    return Response({
        "token": token.key,
        "id": user.id,
        "message": "Login Successfully"
    })
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account(request, format=None):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

