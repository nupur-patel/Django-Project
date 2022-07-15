from rest_framework.exceptions import ValidationError,AuthenticationFailed,NotFound
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import filters as filter_rest
from django_filters import rest_framework as filters

from portfolio_app.api.permissions import IsAdminOrAuthenticatedReadOnly,PortfolioUserOrAdminCanEdit
from portfolio_app.models import Portfolio,ActiveHoldings
from portfolio_app.api.serializers import PortfolioSerializer,ActiveHoldingSerializer
from portfolio_app.api.throttling import BurstPreventionThrottle
from portfolio_app.api.pagination import BasePagination

class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer    
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    filter_backends = (filters.DjangoFilterBackend,filter_rest.SearchFilter)
    # filterset_fields = ()
    search_fields = ('nickname',)
    pagination_class = BasePagination

    def get_queryset(self):
        return Portfolio.objects.filter(Q(is_public = True) | Q(owner = self.request.user))
    def perform_create(self,serializer):
        owner = self.request.user
        
        portfolio_queryset = Portfolio.objects.filter(owner=owner)
        if portfolio_queryset.exists():
            raise ValidationError('Validation Error! Sorry We only support one Portfolio Per user currently!')
        serializer.save(owner = owner)

class PortfolioRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
 
    def get_object(self):
        if self.request.user.is_superuser:
            query_set =  Portfolio.objects.get(pk = self.kwargs['pk']) 
            if query_set.exists():
                return query_set.first()
            else:
                raise NotFound('Portfolio does not exist')
        else:
            query_set = Portfolio.objects.filter(Q(is_public = True) | Q(owner = self.request.user))
            if query_set.exists():
                return query_set.first()
            else:
                raise NotFound('Portfolio is private or doesn\'t exists')

    def perform_update(self,serializer):
        user = self.request.user
        pk = self.kwargs.get('pk',None)
        
        portfolio_queryset = Portfolio.objects.filter(owner=user,pk = pk)
        if portfolio_queryset.exists():
            pass
        else:
            raise ValidationError('Authorization Error. You are not a valid onwer of Portfolio')
        
        serializer.save()

class HoldingListCreateView(generics.ListCreateAPIView):
    serializer_class = ActiveHoldingSerializer
    throttle_class = [BurstPreventionThrottle]
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ActiveHoldings.objects.filter(portfolio = self.kwargs.get('pk'))
        else:
            portfolio = Portfolio.objects.get(id = self.kwargs['pk'])
            if portfolio.owner == self.request.user or portfolio.is_public:
                return ActiveHoldings.objects.filter(Q(portfolio=self.kwargs.get('pk') & (Q(portfolio__is_public = True) | Q(portfolio__owner = self.request.user))))
            else:
                raise AuthenticationFailed('You aren\'t a authorized user to access this portfolio holdings') 

    def perform_create(self,serializer):
        pk = self.kwargs['pk']
        try:
            portfolio = Portfolio.objects.get(pk = pk)
        except Portfolio.DoesNotExist:
            raise NotFound('Portfolio does not exist')
        user = self.request.user
        if self.request.user.is_staff or self.request.user.is_superuser or portfolio.owner == self.request.user: 
            serializer.save(portfolio = portfolio)
        else:
            raise AuthenticationFailed('You aren\'t a authorized user to access this portfolio holdings') 

class HolidingRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActiveHoldingSerializer
    throttle_classes = [BurstPreventionThrottle]
    permission_classes = [PortfolioUserOrAdminCanEdit]

    def get_object(self):
        if self.request.user.is_superuser:
            holiding_queryset =  ActiveHoldings.objects.filter(portfolio=self.kwargs.get('pk'),id = self.kwargs.get('id'))           
            if holiding_queryset.exists():
                return holiding_queryset.first()
            else:
                raise NotFound('This holding doesn\'t exists')
        else:
            holiding_queryset =  ActiveHoldings.objects.filter(portfolio=self.kwargs.get('pk'),id = self.kwargs.get('id')).filter(Q(portfolio__is_public = True) | Q(portfolio__owner = self.request.user))
            if holiding_queryset.exists():
                return holiding_queryset.first()
            else:
                raise NotFound('The holding doesn\'t exist or it is not public ')

    def perform_update(self,serializer):
        user = self.request.user
        pk = self.kwargs.get('pk',None)
        id = self.kwargs.get('id',None)

        holding_queryset = ActiveHoldings.objects.filter(portfolio__owner = user,portfolio = pk,pk = id)
        
        if holding_queryset.exists():
            serializer.save()
        else:
            raise ValidationError('Bad Request, Please make sure you are the owner of portfolio, if holding exists')
        
    def perform_destroy(self, serializer):
        user = self.request.user
        pk = self.kwargs.get('pk',None)
        id = self.kwargs.get('id',None)

        holding_queryset = ActiveHoldings.objects.filter(portfolio__owner = user,portfolio = pk,pk = id)        
        
        if holding_queryset.exists():
            holding_queryset.delete()
            
        else:
            raise ValidationError('Bad Request, Please make sure you are the owner of portfolio, if holding exists')
