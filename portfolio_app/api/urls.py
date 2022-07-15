from django.urls import path
from portfolio_app.api.views import PortfolioListCreateView,PortfolioRetriveUpdateDestroyView,HoldingListCreateView,HolidingRetriveUpdateDestroyView

urlpatterns = [
    path('portfolio/',PortfolioListCreateView.as_view(),name ='portfolio-list'),
    path('portfolio/<int:pk>/', PortfolioRetriveUpdateDestroyView.as_view(),name = 'portfolio-detail'),
    path('portfolio/<int:pk>/holdings/',HoldingListCreateView.as_view(),name = 'holdings'),
    path('portfolio/<int:pk>/holdings/<int:id>/', HolidingRetriveUpdateDestroyView.as_view(),name = 'holding-details')
  
]
