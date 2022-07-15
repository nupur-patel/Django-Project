from rest_framework import serializers
from portfolio_app.models import Portfolio,ActiveHoldings

class ActiveHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveHoldings
        exclude = ('portfolio',)

class PortfolioSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    holdings = ActiveHoldingSerializer(many = True,read_only=True)
    class Meta:
        model = Portfolio
        fields = '__all__'
