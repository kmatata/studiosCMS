import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIB.settings")
import django
django.setup()
from django.conf import settings
from django.contrib.auth.models import User, Group
from flats.models import *
from authy.models import *
from faker import Faker
import cv2
from django.utils.crypto import get_random_string

faker = Faker()

passwords = ['A9tAuKs2', 'ElhrG3Oi', '2KsNaQEj', '0Xp5D4pf', 'Fm7GA6iM', 'cbuvqgdh',
                'gbTC5oOM', '1RN6yUc9', 'P2F4kdAC', 'O44MPEcJ',
                  '9WAOZFSZ', 'gKdJK1a9', 'FL7xeklg']

def create_user(i):    
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = f"{first_name}@example.com"    
    user = User.objects.create(username=f'@{first_name}',first_name=first_name,last_name=last_name,
                        email=email,password=passwords[i])
    renterGrp = Group.objects.get(name='renter')
    user.groups.add(renterGrp)
    user.save()
    random_number = faker.random_int(10000000, 99999999)
    user.profile.cell = f'07{random_number}'
    renterNatId = [faker.random_int(2, 9) for _ in range(8)]
    user.renterProfile.natId = "".join(str(natid) for natid in renterNatId)
    user.save()
    return user

def create_renter_inst(tenant,flat):
    renter = RenterInfo.objects.get(renter=tenant)
    rentedUnit = flat    
    payLog = PaymentLog.objects.create(tenant=renter)
    payLog.payment_status = 'complete'
    payLog.flat = rentedUnit
    payLog.save()
    rentedUnit.vacant = False
    rentedUnit.depositPaid = True
    rentedUnit.save()
    water = Water.objects.create(flat=rentedUnit,quantity=faker.random_int(50,200))
    sewage = Sewage.objects.create(flat=rentedUnit,quantity=faker.random_int(100,250))
    payLog.water = water
    payLog.sewage = sewage
    payLog.save()

tenants=[tenant for tenant in User.objects.filter(groups=Group.objects.get(name='renter'))]

tntFlats = []
for i in range(13):
    x = Flat.objects.get(flat_no=f'Flat{i+1}')
    tntFlats.append(x)

for i in range(len(tenants)):    
    create_renter_inst(tenants[i],tntFlats[i])
    print(f'tenant{i+1} filled to flat')







