from rest_framework import serializers
from stock_app.models import Security,Exchange,DividendHistory,DividendAnnouncement


class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        fields = "__all__"
    
class ExchangeSerializer(serializers.ModelSerializer):
    securities = SecuritySerializer(many=True,read_only=True)
    class Meta:
        model = Exchange
        fields = "__all__"
    def create(self,validate_data):
        if len(validate_data['country']) < 3:
            raise serializers.ValidationError("Country Must be at least 3 characters long")
        
        return Exchange.objects.create(**validate_data)

class DividendHistorySerializer(serializers.ModelSerializer):
    security = serializers.SlugRelatedField(read_only=True,slug_field="ticker")
    class Meta:
        model = DividendHistory
        fields = '__all__'

class DividendAnnouncementSerializer(serializers.ModelSerializer):
    security = serializers.SlugRelatedField(read_only=True,slug_field="ticker")
    class Meta:
        model = DividendAnnouncement
        fields = '__all__'



        
        
