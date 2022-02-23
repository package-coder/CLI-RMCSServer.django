
from django.urls import path

from . import views

urlpatterns = [
    path('', views.AccountLoginAPI.as_view(), name='account'),
    path('login', views.AccountLoginAPI.as_view(), name='login'),
    path('logout', views.accountLogout, name='logout')
]