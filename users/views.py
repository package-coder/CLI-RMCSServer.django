from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotAllowed, 
    HttpResponseBadRequest,
    HttpResponseNotFound
)


from django.http.response import JsonResponse
from . serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)
from rest_framework.views import APIView
from rest_framework import (
    authentication, 
    permissions,
    status
)
from rest_framework.authentication import (
    SessionAuthentication, 
    BasicAuthentication
)
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    DjangoModelPermissions
)
from .models import CustomDjangoModelPermission



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_users(request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_user(request, format=None):
    data = request.data
    try:
        username = data['username']
        password = data['password']
    
    except KeyError:
        return Response(status=status.HTTP_403_FORBIDDEN)

    else:
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('/api/users/%s' % user.id)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_user(request, id, format=None):
    user = get_object_or_404(User, pk=id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_user(request, id, format=None):
    user = get_object_or_404(User, pk=id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return redirect('/api/users/%s' % user.id)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request, id, format=None):
    user = get_object_or_404(User, pk=id)
    user.is_active = False 
    user.save()
    return Response({"message": "Data deleted successfully"})




#TODO to delete
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser, DjangoModelPermissions])
def manage_all_users(request, format=None):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data
        try:
            username = data['username']
            password = data['password']
        
        except KeyError:
            return Response(status=status.HTTP_403_FORBIDDEN)

        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            return redirect('/api/users/%s' % user.id)
    

@api_view(['PATCH', 'GET', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser, DjangoModelPermissions])
def manage_user(request, id, format=None):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PATCH':
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect('/api/users/%s' % user.id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user = get_object_or_404(User, pk=id)
        user.is_active = False 
        user.save()
        return Response({"message": "Data deleted successfully"})