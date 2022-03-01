
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.get_all_users, name='get_all_users'),
    path('create/', views.create_user, name='create_user'),
    path('<id>/', include([
        path('', views.get_user), 
        path('update/', views.update_user, name='update_user'),
        path('delete/', views.delete_user, name='delete_user'),
    ]), name='get_user'),
]