from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework import filters as filter_rest
from django_filters import rest_framework as filters

from stock_app.models import Security, Exchange,DividendHistory,DividendAnnouncement 
from stock_app.api.serializers import SecuritySerializer,ExchangeSerializer,DividendHistorySerializer,DividendAnnouncementSerializer

from portfolio_app.api.throttling import BurstPreventionThrottle
from portfolio_app.api.permissions import IsAdminOrAuthenticatedReadOnly,IsAdminOrReadOnly
from portfolio_app.api.pagination import BasePagination


class SecurityListCreateView(generics.ListCreateAPIView):
    queryset = Security.objects.all()
    serializer_class = SecuritySerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    filter_backends = (filters.DjangoFilterBackend,filter_rest.SearchFilter)
    filterset_fields = ('currency', 'exchange__name')
    search_fields = ('ticker',)
    pagination_class = BasePagination
    def perform_create(self,serializer):
        if serializer.validated_data['price'] < 0.001:
            raise ValidationError('Price cannot be less than 0.001')
        if serializer.validated_data['dividend_yeild'] < 0:
            raise ValidationError('Yeild Cannot be negative')
        serializer.save()

class SecurityFetchUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Security.objects.all()
    serializer_class = SecuritySerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    
    def perform_update(self,serializer):
        if serializer.validated_data['price'] < 0.001:
            raise ValidationError('Price cannot be less than 0.001')
        if serializer.validated_data['dividend_yeild'] < 0:
            raise ValidationError('Yeild Cannot be negative')
        serializer.save()

class ExchangeListCreateView(generics.ListCreateAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    filter_backends = (filters.DjangoFilterBackend,filter_rest.SearchFilter)
    filterset_fields = ('country',)
    pagination_class = BasePagination
    
class ExchangeRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrAuthenticatedReadOnly]

class DividendHistoryListView(generics.ListCreateAPIView):
    serializer_class = DividendHistorySerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,filter_rest.SearchFilter)
    filterset_fields = ('security__exchange','security','security__exchange__country',)
    pagination_class = BasePagination
    def get_queryset(self):
        return DividendHistory.objects.filter(security = self.kwargs.get('pk'))

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        try:
            security = Security.objects.get(pk = pk)
        except:
            raise ValidationError('Security Validation Failed')

        dividend_queryset = DividendHistory.objects.filter(security = security,ex_dividend_date = serializer.validated_data['ex_dividend_date'],
                                                      record_date = serializer.validated_data['record_date'])
 
        if dividend_queryset.exists():
            raise ValidationError("dividend already added")
        
        serializer.save(security = security)
 
class DividendHistoryRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DividendHistory.objects.all()
    serializer_class = DividendHistorySerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrReadOnly]

class DividendAnnouncementListView(generics.ListCreateAPIView):
    serializer_class = DividendHistorySerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,filter_rest.SearchFilter)
    filterset_fields = ('security__exchange','security','security__exchange__country',)
    pagination_class = BasePagination
    def get_queryset(self):
        return DividendAnnouncement.objects.filter(security = self.kwargs.get('pk'))

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        try:
            security = Security.objects.get(pk = pk)
            print(security)
        except:
            raise ValidationError('Security Validation Failed')

        dividend_queryset = DividendAnnouncement.objects.filter(security = security,ex_dividend_date = serializer.validated_data['ex_dividend_date'],
                                                      record_date = serializer.validated_data['record_date'])
 
        if dividend_queryset.exists():
            raise ValidationError("dividend already added")
        
        serializer.save(security = security)

class DividendAnnouncementRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DividendAnnouncement.objects.all()
    serializer_class = DividendAnnouncementSerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrReadOnly]
