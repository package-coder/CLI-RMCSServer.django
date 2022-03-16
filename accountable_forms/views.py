from django.shortcuts import get_object_or_404, render
from rest_framework import (
    status,
    generics,
    mixins
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
    AFItem,
    AFTransactionHistory,
    AFTransactionItem,
    AFType,
    AFRequestItem,
    AFRequestHistory
)
from .serializers import(
    AFItemSerializer,
    AFPurchaseRequestSerializer,
    AFRequestItemReadOnlySerializer,
    AFPurchaseTransactionSerializer,
    AFRequestTransactionSerializer,
    AFTransactionSerializer,
    AFTransactionItemReadOnlySerializer,
    AFTransactionItemSerializer,
    AFTypeSerializer,
    AFRequestItemSerializer,
    AFRequestSerializer
)

class NestedReadOnlyGenericAPIView(generics.GenericAPIView):
    read_serializer_class = None

    def get_serializer_class(self):

        if self.request.method in ['GET']:
            return self.read_serializer_class
        return self.serializer_class

class AFTypeListCreateAPI(generics.ListCreateAPIView):
    queryset = AFType.objects.all()
    serializer_class = AFTypeSerializer


class AFTypeItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = AFType.objects.all()
    serializer_class = AFTypeSerializer
    

class AFRequestItemListCreateAPI(generics.ListCreateAPIView, NestedReadOnlyGenericAPIView):
    queryset = AFRequestItem.objects.all()
    serializer_class = AFRequestItemSerializer
    read_serializer_class = AFRequestItemReadOnlySerializer


class AFRequestItemAPI(generics.RetrieveUpdateDestroyAPIView, NestedReadOnlyGenericAPIView):
    queryset = AFRequestItem.objects.all()
    serializer_class = AFRequestItemSerializer
    read_serializer_class = AFRequestItemReadOnlySerializer


class AFRequestHistoryListCreateAPI(generics.ListCreateAPIView):
    queryset = AFRequestHistory.objects.all()
    serializer_class = AFRequestSerializer

    def get_serializer_class(self):
        if self.request.method in ['GET']: 
            return self.serializer_class

        request_type = self.request.data['request_type']
        if request_type == 'TYPE_PURCHASE':
            return AFPurchaseRequestSerializer

        return self.serializer_class


class AFRequestHistoryItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = AFRequestHistory.objects.all()
    serializer_class = AFRequestSerializer


class AFTransactionHistoryListCreateAPI(generics.ListCreateAPIView):
    queryset = AFTransactionHistory.objects.all()
    serializer_class = AFTransactionSerializer

    def get_serializer_class(self):
        if self.request.method in ['GET']: 
            return self.serializer_class

        if 'request_history' in self.request.data.keys():
            return AFRequestTransactionSerializer

        transaction_type = self.request.data['transaction_type']
        if transaction_type == 'TYPE_PURCHASE':
            return AFPurchaseTransactionSerializer

        return self.serializer_class

class AFTransactionHistoryItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = AFTransactionHistory.objects.all()
    serializer_class = AFRequestTransactionSerializer


class AFTransactionItemListCreateAPI(generics.ListCreateAPIView, NestedReadOnlyGenericAPIView):
    queryset = AFTransactionItem.objects.all()
    serializer_class = AFTransactionItemSerializer
    read_serializer_class = AFTransactionItemReadOnlySerializer


class AFTransactionItemAPI(generics.RetrieveUpdateDestroyAPIView, NestedReadOnlyGenericAPIView):
    queryset = AFTransactionItem.objects.all()
    serializer_class = AFTransactionItemSerializer
    read_serializer_class = AFTransactionItemReadOnlySerializer


class AFItemListAPI(generics.ListAPIView):
    queryset = AFItem.objects.all()
    serializer_class = AFItemSerializer