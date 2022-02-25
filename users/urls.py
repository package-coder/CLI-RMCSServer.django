
from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all_users, name='get_all_users'),
    path('create/', views.create_user, name='create_user'),
    path('<id>', views.get_user, name='get_user'),
    path('<id>/update/', views.update_user, name='update_user'),
    path('<id>/delete/', views.delete_user, name='delete_user'),
]