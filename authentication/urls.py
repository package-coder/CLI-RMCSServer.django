
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.accountLogin, name='login'),
    path('logout', views.accountLogout, name='logout'),
    path('', views.account, name='account'),
    path('cookies', views.cookies)
]