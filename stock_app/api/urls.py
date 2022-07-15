from django.urls import path, include
from stock_app.api.views import (SecurityListCreateView,SecurityFetchUpdateDeleteView,ExchangeListCreateView,
                                 ExchangeRetrieveUpdateView,DividendHistoryListView,DividendHistoryRetrieveUpdateView,
                                 DividendAnnouncementListView,DividendAnnouncementRetrieveUpdateView)

urlpatterns = [
    path('security/', SecurityListCreateView.as_view(),name = 'security-list'),
    path('security/<int:pk>/', SecurityFetchUpdateDeleteView.as_view(),name = 'security-detail'),
  
    path('exchange/',ExchangeListCreateView.as_view(),name='exchange-list'),
    path('exchange/<int:pk>/', ExchangeRetrieveUpdateView.as_view(),name = 'exchange-detail'),
  
    path('security/<int:pk>/historical-dividends/',DividendHistoryListView.as_view(),name = 'historical-dividends'),
    path('historical-dividends/<int:pk>/', DividendHistoryRetrieveUpdateView.as_view(),name = 'historical-dividends-detail'),
  
    path('security/<int:pk>/upcoming-dividends',DividendAnnouncementListView.as_view(),name = 'dividend-announcement'),
    path('upcoming-dividends/<int:pk>/',DividendAnnouncementRetrieveUpdateView.as_view(),name = 'dividend-announcement-detail')
  
  
]


# Exchange->Post securities