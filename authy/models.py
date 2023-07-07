from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from PIL import Image
from django.utils import timezone
import os
from django.conf import settings


def render_id_image_dir_path(instance, filename):
    imgageFile = filename.split('.')
    try:
        if (imgageFile[-1] == 'jpeg'):
            image_ext = '.jpeg'
        elif (imgageFile[-1] == 'png'):
            image_ext = '.png'
        elif (imgageFile[-1] == 'jpg'):
            image_ext = '.jpg'        
    except Exception as e:
        raise e
    image_ext_name = '{0}/user_{1}/NatId{2}'.format(instance.renter.first_name,instance.natId,image_ext)
    full_path  = os.path.join(settings.MEDIA_ROOT, image_ext_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)    
    return image_ext_name

def render_tax_info_dir_path(instance, filename):
    imgageFile = filename.split('.')
    try:
        if (imgageFile[-1] == 'jpeg'):
            image_ext = '.jpeg'
        elif (imgageFile[-1] == 'png'):
            image_ext = '.png'
        elif (imgageFile[-1] == 'jpg'):
            image_ext = '.jpg'
        
    except Exception as e:
        raise e
    image_ext_name = '{0}/user_{1}/taxinfo{2}'.format(instance.renter.first_name,instance.natId,image_ext)
    full_path  = os.path.join(settings.MEDIA_ROOT, image_ext_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)    
    return image_ext_name

def invoice_dir(instance, filename):
    return '{0}/user_{1}/invce/% Y/% m/% d/{2}'.format(instance.renter.first_name,instance.natId,filename)


class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  cell = PhoneNumberField(unique=True,region="KE",null=True,blank=True)

  def __str__(self):
    return self.user.first_name
  
class RenterInfo(models.Model):
   renter = models.OneToOneField(User,on_delete=models.CASCADE, related_name='renterProfile')
   natId = models.CharField(max_length=8, verbose_name='National ID', unique=True, validators=[RegexValidator(r'^[0-9]+$')],null=True,default=None,blank=True)    
   taxinfo = models.ImageField(upload_to=render_tax_info_dir_path,default=None,null=True,blank=True)
   renterImage_id = models.ImageField(upload_to=render_id_image_dir_path,default=None,null=True,blank=True)   
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   
   def save(self,*args,**kwargs):        
        super().save(*args,**kwargs)        
        SIZE = 630,1024
        if self.renterImage_id or self.taxinfo:
            if self.renterImage_id:
                img = Image.open(self.renterImage_id.path)
                img.thumbnail(size=(SIZE))
                img.save(self.renterImage_id.path,optimize=True,qulaity=90)
            elif self.taxinfo:
                img2 = Image.open(self.taxinfo.path)
                img2.thumbnail(size=(SIZE))
                img2.save(self.taxinfo.path,optimize=True,quality=90)
    
   def __str__(self):
        return f"{self.renter.first_name} {self.renter.last_name}"

class PaymentLog(models.Model):
    tenant = models.ForeignKey(RenterInfo, on_delete=models.SET_NULL, default=None, null=True,blank=True,related_name='payments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=10, default='pending',choices=[
        ('complete', 'Complete'), ('pending', 'Pending'), 
        ('processing', 'Processing'), ('rejected', 'Rejected')])    
    renterInvoice = models.FileField(upload_to=invoice_dir,default=None,null=True,blank=True)
    flat = models.ForeignKey('flats.Flat',on_delete=models.SET_NULL,
                               blank=True,null=True,default=None,related_name='flat')
    water = models.OneToOneField('flats.Water',on_delete=models.SET_NULL, null=True, blank=True,related_name='water')
    sewage = models.OneToOneField('flats.Sewage',on_delete=models.SET_NULL, null=True, blank=True,related_name='sewage')
    active = models.BooleanField(default=True)
    

    def __str__(self) -> str:
        return f'{self.tenant}'
    @property
    def get_total_cost(self):
        if not self.flat.depositPaid:
            return self.flat.rentalFee + self.flat.threeMonthDeposit
        else:
            rentalFee = self.flat.rentalFee            
            water = self.water.get_cost
            sewage = self.sewage.get_cost                
            return rentalFee + water + sewage + self.flat.maintenaceFee


def profile_save(sender, created, instance, *args, **kwargs):        
    if created:
        Profile.objects.create(user=instance)        
    else:
        instance.profile.save()        
        try:
            if instance.groups.values('name')[0]['name'] == 'renter':
                renter,create = RenterInfo.objects.get_or_create(renter=instance)                            
                if not create:
                    renter.save()
        except IndexError:
            pass        

    
    


post_save.connect(profile_save, sender=User)
