
from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_account, name='get_account'),
    path('login', views.login_account, name='login_account'),
    path('logout', views.logout_account, name='logout_account')
]