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

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.middleware import csrf
from users.serializers import UserSerializer

def accountLogin(request):

    if request.method=='POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        
        except (KeyError, ObjectDoesNotExist):
            return HttpResponseBadRequest("Cannot find the required credential")
        
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                serializer = UserSerializer(User.objects.get(pk=request.user.id))
                return JsonResponse(serializer.data, safe=False)
            else:
                return HttpResponseBadRequest('Authentication Failed')
    
    if request.method=='GET' and request.user.is_authenticated:
        serializer = UserSerializer(User.objects.get(pk=request.user.id))
        return JsonResponse(serializer.data, safe=False)
    
    return HttpResponseBadRequest('No current user is logged in')
    
def accountLogout(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    logout(request)
    return HttpResponse("Logout Successfully")

def account(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed('Not allowed to make the request')

    serializer = UserSerializer(User.objects.get(pk=request.user.id))
    return JsonResponse(serializer.data, safe=False)

def cookies(request):
    user = authenticate(username='chris', password='admin101')
    login(request, user)
    
    return HttpResponse(csrf.get_token(request))