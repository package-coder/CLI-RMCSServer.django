
from django.urls import path, include

from .views import (
    AFItemListAPI,
    AFRequestHistoryItemAPI,
    AFRequestHistoryListCreateAPI,
    AFTransactionHistoryItemAPI,
    AFTransactionHistoryListCreateAPI,
    AFTransactionItemAPI,
    AFTransactionItemListCreateAPI,
    AFTypeItemAPI,
    AFTypeListCreateAPI,
    AFRequestItemAPI,
    AFRequestItemListCreateAPI,
)

urlpatterns = [
    
    #   Accountable Forms - Types API
    path('types/', include([
        path('', AFTypeListCreateAPI.as_view(), name='AFTypeListCreateAPI'),
        path('<int:pk>/', AFTypeItemAPI.as_view(), name='AFTypeListCreateAPI'),
    ])),


    #   Accountable Forms - Requests History API
    path('requests/', include([
        path('', AFRequestHistoryListCreateAPI.as_view(), name='AFRequestHistoryListCreateAPI'),
        path('<pk>/', AFRequestHistoryItemAPI.as_view(), name='AFRequestHistoryItemAPI'),
    ])),

    #   Accountable Forms - Request Items API
    path('request_items/', include([
        path('', AFRequestItemListCreateAPI.as_view(), name='AFRequestItemListCreateAPI'),
        path('<pk>/', AFRequestItemAPI.as_view(), name='AFRequestItemAPI'),
    ])),


    #   Accountable Forms - Transaction History API
    path('transactions/', include([
        path('', AFTransactionHistoryListCreateAPI.as_view(), name='AFTransactionHistoryListCreateAPI'),
        path('<pk>/', AFTransactionHistoryItemAPI.as_view(), name='AFTransactionHistoryItemAPI'),
    ])),

    #   Accountable Forms - Transaction Items API
    path('transaction_items/', include([
        path('', AFTransactionItemListCreateAPI.as_view(), name='AFTransactionItemListCreateAPI'),
        path('<pk>/', AFTransactionItemAPI.as_view(), name='AFTransactionItemAPI'),
    ])),
    
    path('af_items/', include([
        path('', AFItemListAPI.as_view(), name='AFItemListAPI'),
    ]))

]   