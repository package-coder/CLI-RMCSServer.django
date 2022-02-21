from django.shortcuts import render
from django.http import (
    HttpResponse, 
    HttpResponseNotAllowed, 
    HttpResponseBadRequest
)

from django.http.response import JsonResponse
from . serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.
def index(request):

    users = User.objects.all()
    usersSerial = UserSerializer(users, many=True)
    return JsonResponse(usersSerial.data, safe=False)