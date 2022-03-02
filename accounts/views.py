from django.shortcuts import (
    get_object_or_404
)

from django.contrib.auth import (
    logout, 
    authenticate,
    login
)

from django.contrib.auth.models import (
    Group, 
    Permission
)


from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import (
    status, 
    generics
)

from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny
)

from .serializers import (
    GroupSerializer,
    PermissionSerializer, 
    UserSerializer
)

from .models import User


@api_view()
@permission_classes([IsAuthenticated])
def logout_account(request):

    logout(request)
    token = Token.objects.get(pk=request.auth)
    token.delete()
    return Response({
        'message': 'Logout successfully'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_account(request, format=None):

    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
        token.delete()

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




class UserListCreateAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDestroyAPI(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupListCreateAPI(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GroupRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PermissionListAPI(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class PermissionRetrieveAPI(generics.RetrieveAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]






@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_users(request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
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
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request, id, format=None):
    user = get_object_or_404(User, pk=id)
    user.is_active = False 
    user.save()
    return Response({"message": "Data deleted successfully"})

