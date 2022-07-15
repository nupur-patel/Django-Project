from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from stock_app.api import serializers
from stock_app import models
import datetime


# TEST Case for ExchangeListCreateView

class ExchangeListCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_user_exchange_list(self):
        response = self.client.get(reverse('exchange-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_annon_user_exchange_list(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('exchange-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_staff_user_exchange_create(self):
        data = {
            "country":"Canada",
            "name":"TSX"
        }
        response = self.client.post(reverse('exchange-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_staff_or_super_user_exchange_create(self):        
        self.user.is_superuser = True
        self.user.save()
        data = {
            "country":"Canada",
            "name":"TSX"
        }
        response = self.client.post(reverse('exchange-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_invalid_country_name_exchange_create(self):
        self.user.is_superuser  = True
        self.user.save()
        data = {
            "Country":"India", #Invalid name
            "name":"TSX"
        }
        response = self.client.post(reverse('exchange-list'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class ExchangeRetrieveUpdateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.exchange = models.Exchange.objects.create(name='KE',country='Canada')
        
    def test_anon_user_access_exchange_obj(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('exchange-detail', args=(self.exchange.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_staff_user_access_exchange_obj(self):
        response = self.client.get(reverse('exchange-detail', args=(self.exchange.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_staff_user_update_exchange_obj(self):
        data = {
            "country":"Canada",
            "name":"TSX"
        } 
        response = self.client.put(reverse('exchange-detail', args=(self.exchange.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_delete_exchange_obj(self):
        response = self.client.delete(reverse('exchange-detail', args=(self.exchange.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_access_exchange_obj(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(reverse('exchange-detail', args=(self.exchange.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_update_exchange_obj(self):
        self.user.is_superuser = True
        self.user.save()
        data = {
            "country":"Canada",
            "name":"TSX"
        } 
        response = self.client.put(reverse('exchange-detail', args=(self.exchange.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_superuser_delete_exchange_obj(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.delete(reverse('exchange-detail', args=(self.exchange.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_update_exchange_obj_with_invalid_country(self):
        self.user.is_superuser = True
        self.user.save()
        data = {
            "country":"India",
            "name":"TSX"
        } 
        response = self.client.put(reverse('exchange-detail', args=(self.exchange.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class SecurityListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.exchange = models.Exchange.objects.create(name='KE',country='Canada')
        self.security = models.Security.objects.create(exchange=self.exchange,price=3.3,dividend_yeild = 2,
                                                       ticker = 'ENS.TO',yearly_dividend_amt='1.2',
                                                       dividend_frequency='Monthly',currency='CAD')

    def test_annon_user_access_security_list(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('security-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_annon_user_access_security_create(self):
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('security-list'),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_access_security_create(self):
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        response = self.client.post(reverse('security-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_regular_user_access_security_list(self):
        response = self.client.get(reverse('security-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_access_security_list(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(reverse('security-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_access_security_create(self):
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        self.user.is_superuser = True
        self.user.save()
        response = self.client.post(reverse('security-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_superuser_create_with_invalid_data(self):
        self.user.is_superuser = True
        self.user.save()
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        
        data['dividend_yeild'] = -12.3
        response = self.client.post(reverse('security-list'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        data['dividend_yeild'] = 2.3
        data['price'] = -32.4
        response = self.client.post(reverse('security-list'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        data['exchange'] =  32323
        response = self.client.post(reverse('security-list'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class SecurityFetchUpdateDeleteViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.exchange = models.Exchange.objects.create(name='KE',country='Canada')
        self.security = models.Security.objects.create(exchange=self.exchange,price=3.3,dividend_yeild = 2,
                                                       ticker = 'ENS.TO',yearly_dividend_amt='1.2',
                                                       dividend_frequency='Monthly',currency='CAD')
    # Anon User test case
    def test_annon_user_access_security_obj(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('security-detail', args=(self.security.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_annon_user_update_security_obj(self):
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('security-detail', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_annon_user_delete_security_obj(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse('security-detail', args=(self.security.id,)))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    
    # Regular User Testcase
    
    def test_regular_user_update_security_obj(self):
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        response = self.client.put(reverse('security-detail', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_regular_user_access_security_obj(self):
        response = self.client.get(reverse('security-detail', args=(self.security.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_delete_security_obj(self):
        response = self.client.delete(reverse('security-detail', args=(self.security.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    def test_superuser_access_exchange_obj(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(reverse('security-detail', args=(self.security.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_update_exchange_obj(self):
        self.user.is_superuser = True
        self.user.save()
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        response = self.client.put(reverse('security-detail', args=(self.security.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_superuser_delete_exchange_obj(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.delete(reverse('security-detail', args=(self.security.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_update_with_invalid_data(self):
        self.user.is_superuser = True
        self.user.save()
        data = {
            "exchange":self.exchange.id,
            "price":32.32,
            "dividend_yeild":3.4,
            "ticker":'EMS.TO',
            "yearly_dividend_amt":1.2,
            "dividend_frequency":"Monthly",
            "currency":"CAD"
        }
        
        data['dividend_yeild'] = -12.3
        response = self.client.put(reverse('security-detail', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        data['dividend_yeild'] = 2.3
        data['price'] = -32.4
        response = self.client.put(reverse('security-detail', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        data['exchange'] =  32323
        response = self.client.put(reverse('security-detail',args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class DividendHistoryListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.exchange = models.Exchange.objects.create(name='KE',country='Canada')
        self.security = models.Security.objects.create(exchange=self.exchange,price=3.3,dividend_yeild = 2,
                                                       ticker = 'ENS.TO',yearly_dividend_amt='1.2',
                                                       dividend_frequency='Monthly',currency='CAD')
        self.dividend_history = models.DividendHistory.objects.create(security = self.security,payment_date = datetime.date(2022,3,3),
                                                       announcement_date = datetime.date(2022,3,3),record_date = datetime.date(2022,2,2),
                                                       ex_dividend_date = datetime.date(2022,3,3),type = "Special",amount = 2,
                                                       currency = "CAD")
        
    
    
    def test_annon_user_access_divi_history_list(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('historical-dividends', args=(self.security.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_annon_user_access_divi_history_create(self):
        data = {
            "security":self.security.id,
            "payment_date":datetime.date(2022,3,3),
            "announcement_date":datetime.date(2022,3,3),
            "record_date":datetime.date(2022,3,3),
            "ex_dividend_date":datetime.date(2022,3,3),
            "type":"Monthly",
            "currency":"CAD",
            "amount":2
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('historical-dividends', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_access_divi_history_create(self):
        data = {
            "payment_date":datetime.date(2022,3,3),
            "announcement_date":datetime.date(2022,3,3),
            "record_date":datetime.date(2022,3,3),
            "ex_dividend_date":datetime.date(2022,3,3),
            "type":"Monthly",
            "currency":"CAD",
            "amount":2
        }
        response = self.client.post(reverse('historical-dividends', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_regular_user_access_divi_history_list(self):
        response = self.client.get(reverse('historical-dividends', args=(self.security.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_access_divi_history_list(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(reverse('historical-dividends', args=(self.security.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_access_divi_history_create(self):
        data = {
            "payment_date":datetime.date(2022,3,13),
            "announcement_date":datetime.date(2022,3,13),
            "record_date":datetime.date(2022,3,13),
            "ex_dividend_date":datetime.date(2022,3,13),
            "type":"Monthly",
            "currency":"CAD",
            "amount":2
        }
        self.user.is_superuser = True
        self.user.save()
        response = self.client.post(reverse('historical-dividends', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_superuser_create_historical_dividend_with_invalid_data(self):
        self.user.is_superuser = True
        self.user.save()
        data = {
            "payment_date":datetime.date(2022,3,13),
            "announcement_date":datetime.date(2022,3,13),
            "record_date":datetime.date(2022,3,3),
            "ex_dividend_date":datetime.date(2022,3,13),
            "type":"Monthly",
            "currency":"CAD",
            "amount":2
        }
        
        # Security ID Invalid -
        response = self.client.post(reverse('historical-dividends', args=(333,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        # add same dividend date & record date again for given security
        data = {
            "payment_date":datetime.date(2022,3,3),
            "announcement_date":datetime.date(2022,3,13),
            "record_date":datetime.date(2022,2,2),
            "ex_dividend_date":datetime.date(2022,3,3),
            "type":"Monthly",
            "currency":"CAD",
            "amount":2
        }
        response = self.client.post(reverse('historical-dividends', args=(self.security.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


