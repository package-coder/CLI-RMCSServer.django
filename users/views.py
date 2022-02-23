from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (
    render,
    get_object_or_404
)
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
from rest_framework.views import APIView
from rest_framework import (
    authentication, 
    permissions,
    status
)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser
)


# Create your views here.
class UserAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, userId=None, format=None):
        if userId is None:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        
        user = get_object_or_404(User, pk=userId)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        data = request.data
        try:
            username = data['username']
            password = data['password']
        
        except KeyError:
            return Response(status=status.HTTP_403_FORBIDDEN)

        else:
            user = User.objects.create_user(username=username, password=password)
            user.email = data.get('email', '')
            user.firstname = data.get('firstname', '')
            user.lastname = data.get('lastname', '')
            user.save()

            return Response({
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)