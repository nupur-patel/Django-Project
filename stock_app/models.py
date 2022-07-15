from django.db import models
from django.core.exceptions import ValidationError

COUNTRY_CHOICES = [('Canada','Canada'),('USA','USA')]

# Create your models here.
class Security(models.Model):
    exchange = models.ForeignKey('Exchange',related_name = 'securities', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=13, decimal_places=3,default = 0.0)
    dividend_yeild = models.DecimalField(max_digits=6, decimal_places=3,default = 0.0)
    ticker = models.CharField(max_length=20,blank = True,null = True)
    yearly_dividend_amt = models.DecimalField(max_digits=10,decimal_places=3,default = 0.0)
    dividend_frequency = models.CharField(max_length=20,default = 'Monthly')
    currency = models.CharField(max_length=4,default = 'CAD')
    
    def clean(self):
        if self.price < 0.001:
            raise ValidationError('Please enter price > 0.001')
        if self.dividend_yeild < 0:
            raise ValidationError('Yeild Cannot be negative')
    def __str__(self):
        return self.ticker

    
class Exchange(models.Model):
    country = models.CharField(max_length=40,choices=COUNTRY_CHOICES)
    name = models.CharField(max_length=40,default = 'TSX')
    
    def __str__(self):
        return self.name
    
class DividendHistory(models.Model):
    security = models.ForeignKey(Security,on_delete=models.CASCADE,related_name='dividend_history')
    payment_date = models.DateField()
    announcement_date = models.DateField()
    record_date = models.DateField()
    ex_dividend_date = models.DateField() 
    amount = models.DecimalField(max_digits=10, decimal_places= 3)
    type = models.CharField(max_length=40,default = 'TSX')
    currency = models.CharField(max_length=3,default = 'CAD')
    
    def __str__(self):
        return self.security.ticker

class DividendAnnouncement(models.Model):
    security = models.ForeignKey(Security,on_delete=models.CASCADE)
    payment_date = models.DateField()
    announcement_date = models.DateField()
    record_date = models.DateField()
    ex_dividend_date = models.DateField() 
    amount = models.DecimalField(max_digits=10, decimal_places= 3)
    type = models.CharField(max_length=40,default = 'TSX')
    currency = models.CharField(max_length=3,default = 'CAD')

    def __str__(self):
        return self.security.ticker