from os import stat
from django.shortcuts import get_object_or_404, render
from rest_framework import (
    status,
    generics
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import (
    IsAdminUser,
    DjangoModelPermissions
)

from rest_framework.response import Response

from .permissions import ExtendedDjangoModelPermissions
from .models import (
    AFType,
    AFRequestItem,
    AFRequestHistory
)
from .serializers import(
    AFTypeSerializer,
    AFRequestItemSerializer,
    AFRequestHistorySerializer
)


class AFTypeListCreateAPI(generics.ListCreateAPIView):
    queryset = AFType.objects.all()
    serializer_class = AFTypeSerializer

class AFTypeItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = AFType.objects.all()
    serializer_class = AFTypeSerializer
    

class AFRequestItemListCreateAPI(generics.ListCreateAPIView):
    queryset = AFRequestItem.objects.all()
    serializer_class = AFRequestItemSerializer

class AFRequestItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = AFRequestItem.objects.all()
    serializer_class = AFRequestItemSerializer


class AFRequestHistoryListCreateAPI(generics.ListCreateAPIView):
    queryset = AFRequestHistory.objects.all()
    serializer_class = AFRequestHistorySerializer

class AFRequestHistoryItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = AFRequestHistory.objects.all()
    serializer_class = AFRequestHistorySerializer
