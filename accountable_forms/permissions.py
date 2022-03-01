from rest_framework import permissions

class ExtendedDjangoModelPermissions(permissions.DjangoModelPermissions):
    view_permissions = ['%(app_label)s.view_%(model_name)s']

    perms_map = {
        'GET': view_permissions,
        'OPTIONS': view_permissions,
        'HEAD': view_permissions,
        'POST': permissions.DjangoModelPermissions.perms_map['POST'],
        'PUT': permissions.DjangoModelPermissions.perms_map['PUT'],
        'PATCH': permissions.DjangoModelPermissions.perms_map['PATCH'],
        'DELETE': permissions.DjangoModelPermissions.perms_map['DELETE'],
    }