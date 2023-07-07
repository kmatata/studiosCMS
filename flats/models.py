from django.db import models
from authy.models import PaymentLog
import re

class Flat(models.Model):
    flat_no = models.CharField(max_length=10)    
    vacant = models.BooleanField(default=True)
    rentalFee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maintenaceFee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    threeMonthDeposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
    depositPaid = models.BooleanField(default=False)    
    date = models.DateTimeField(auto_now=True)
    waterUnitCost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sewageUnitCost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nos_of_bedrooms = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Flat'
        verbose_name_plural = 'Flats'

    def __str__(self):
        return  re.findall(r"\d+$", self.flat_no)[0]

class Water(models.Model):
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now=True)
    flat = models.ForeignKey(Flat,on_delete=models.SET_NULL,
                               blank=True,null=True,default=None,related_name='water')
    @property
    def get_cost(self):
        return self.unitPrice * self.quantity

class Sewage(models.Model):
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now=True)    
    flat = models.ForeignKey(Flat,on_delete=models.SET_NULL,
                               blank=True,null=True,default=None,related_name='sewage')
    @property
    def get_cost(self):
        return self.unitPrice * self.quantity