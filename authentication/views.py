from django.contrib.auth.models import User
from django.shortcuts import (
    render,
    redirect
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

from django.http.response import JsonResponse
from users.serializers import UserSerializer

def accountLogin(request):
    if request.method=='POST':
        try:
            username = request.POST['username']
            password = request.POST['password']

        except (KeyError):
            return HttpResponseNotAllowed("Can't find the required credential")

        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                serializer = UserSerializer(User.objects.get(pk=request.user.id))
                return HttpResponse(JsonResponse(serializer.data, safe=False), "Login Successfully")
            else:
                return HttpResponseBadRequest("Authentication Failed")

    serializer = UserSerializer(User.objects.get(pk=request.user.id))
    return JsonResponse(serializer.data, safe=False)
    
def accountLogout(request):

    if request.user is None:
        redirect('/login/')

    logout(request)
    return HttpResponse("Logout Successfully")
