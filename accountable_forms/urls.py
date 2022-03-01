
from django.urls import path, include

from .views import (
    AFRequestHistoryItemAPI,
    AFRequestHistoryListCreateAPI,
    AFTypeItemAPI,
    AFTypeListCreateAPI,
    AFRequestItemAPI,
    AFRequestItemListCreateAPI,
)

urlpatterns = [
    path('types/', AFTypeListCreateAPI.as_view(), name='AFTypeListCreateAPI'),
    path('type/<int:id>/', AFTypeItemAPI.as_view(), name='AFTypeListCreateAPI'),
    path('request_items/', AFRequestItemListCreateAPI.as_view(), name='AFRequestItemListCreateAPI'),
    path('request_item/<int:id>/', AFRequestItemAPI.as_view(), name='AFRequestItemAPI'),
    path('requests/', AFRequestHistoryListCreateAPI.as_view(), name='AFRequestListCreateAPI'),
    path('request/<int:id>', AFRequestHistoryItemAPI.as_view(), name='AFRequestHistoryItemAPI'),
]