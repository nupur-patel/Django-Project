from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from stock_app.api import serializers
from stock_app import models

class SecurityListCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'example',password = "password@P123")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)
        
    def test_exchange_create(self):
        data = {
            "country":"CANADA",
            "name":"TSX"
        }
        
        response = self.client.post(reverse('exchange-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        '''
        
           exchange = models.ForeignKey('Exchange',related_name = 'securities', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=13, decimal_places=3,default = 0.0)
    dividend_yeild = models.DecimalField(max_digits=6, decimal_places=3,default = 0.0)
    ticker = models.CharField(max_length=20,blank = True,null = True)
    yearly_dividend_amt = models.DecimalField(max_digits=10,decimal_places=3,default = 0.0)
    dividend_frequency = models.CharField(max_length=20,default = 'Monthly')
    currency = m
    
    class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        fields = "__all__"
    
        '''