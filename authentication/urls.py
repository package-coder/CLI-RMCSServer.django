
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.accountLogin),
    path('logout', views.accountLogout),
]