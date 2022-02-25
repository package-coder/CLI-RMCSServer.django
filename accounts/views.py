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
    IsAdminUser
)

import json
from users.serializers import UserSerializer


@api_view()
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def logout_account(request):
    logout(request)
    return Response({
        'message': 'Logout successfully'
    })


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def login_account(request, format=None):
    print(request.data)

    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        return Response(status=status.HTTP_403_FORBIDDEN)
    else:
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

        login(request, user)
        return Response({"message": "Login successfully"})
        


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_account(request, format=None):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

