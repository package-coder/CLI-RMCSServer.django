from django.urls import include, path

from .views import (
    get_account,
    login_account,
    logout_account,
    UserDestroyAPI,
    UserRetrieveUpdateAPI,
    UserListCreateAPI,
    GroupRetrieveUpdateDestroyAPI,
    GroupListCreateAPI,
    PermissionRetrieveAPI,
    PermissionListAPI
)


urlpatterns = [
    path('', get_account, name='get_account'),
    path('login/', login_account, name='login_account'),
    path('logout/', logout_account, name='logout_account'),

    path('user/<pk>', UserRetrieveUpdateAPI.as_view(), name='UserRetrieveUpdateAPI'),
    path('user/<pk>', UserDestroyAPI.as_view(), name='UserDestroyAPI'),
    path('users/', UserListCreateAPI.as_view(), name="UserListCreateAPI"),
    path('role/<pk>', GroupRetrieveUpdateDestroyAPI.as_view(), name='GroupRetrieveUpdateDestroyAPI'),
    path('roles/', GroupListCreateAPI.as_view(), name='GroupListCreateAPI'),
    path('permission/<pk>', PermissionRetrieveAPI.as_view(), name='PermissionRetrieveAPI'),
    path('permissions/', PermissionListAPI.as_view(), name='PermissionListAPI'),
]