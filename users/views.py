from django.shortcuts import (
    redirect,
    get_object_or_404
)
from . serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.views import APIView
from rest_framework import (
    status,
    generics
)
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    DjangoModelPermissions
)

#USERS VIEW
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_user(request, format=None):

    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.create(serializer.validated_data)
    user.save()

    return Response({ "id": user.id },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def get_user(request, id, format=None):
    user = get_object_or_404(User, pk=id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_user(request, id, format=None):
    user = get_object_or_404(User, pk=id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    user = serializer.update(serializer.validated_data)
    user.save()
    return Response({ "message": "Updated Successfully" })

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, id, format=None):
    user = get_object_or_404(User, pk=id)
    user.is_active = False 
    user.save()
    return Response({"message": "Data deleted successfully"})

