
from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_all_users, name='manage_all_users'),
    path('<id>', views.manage_user, name='manage_user'),
]