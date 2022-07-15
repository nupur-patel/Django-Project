from django.db import models
from django.contrib.auth.models import User
from stock_app.models import Security
# Create your models here.

class Portfolio(models.Model):
    nickname = models.CharField(max_length=20,blank=True,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    market_value = models.DecimalField(max_digits=19, decimal_places= 3,default = 0) 
    change_percentage = models.DecimalField(max_digits=7,decimal_places=2,default = 0)
    initial_deposit_cost =  models.DecimalField(max_digits=19, decimal_places= 3,default = 0) 
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nickname

class ActiveHoldings(models.Model):
    portfolio = models.ForeignKey(Portfolio,on_delete=models.CASCADE,related_name='holdings')
    securities = models.ForeignKey(Security,on_delete=models.CASCADE)
    purchase_price_for_security = models.DecimalField(max_digits=19, decimal_places= 3,default=0) 
    security_qty = models.PositiveBigIntegerField(default = 0)
    dividend_amount_received_total = models.DecimalField(max_digits=19, decimal_places= 3,default = 0) 
    yeild_on_cost = models.DecimalField(max_digits=6, decimal_places= 3,default = 0) 
    yeild = models.DecimalField(max_digits=6, decimal_places= 3,default = 0)
    total_investment = models.DecimalField(max_digits=19, decimal_places= 3,default = 0) 
    current_value = models.DecimalField(max_digits=19, decimal_places=3, default = 0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.portfolio.nickname +  ':' + self.securities.ticker

