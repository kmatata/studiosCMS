from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django_tables2.views import SingleTableMixin, SingleTableView
from .models import RenterInfo,PaymentLog
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .tables import RenterInfoTable, PaymentLogTable
from .filters import RenterPaymentUniversalFilter
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django.db.models import Q

def owner(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            firstNme = user_form.cleaned_data.get('firstName')
            lastNme = user_form.cleaned_data.get('lastName')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            user = User.objects.create_user(username=f'@{lastNme}', is_staff=True, first_name=firstNme, last_name=lastNme, email=email, password=password)            
            user.set_password(user_form.cleaned_data['password'])                             
            user.save()   
            user.groups.add(Group.objects.get(name='owner'))
            user.save()
            login(request, user)
            return redirect('authy:tenant_table')
    else:
        user_form = UserRegistrationForm()

    return render(request,"signup/owner_signup.html",{'form':user_form})

def sales(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            firstNme = user_form.cleaned_data.get('firstName')
            lastNme = user_form.cleaned_data.get('lastName')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            user = User.objects.create_user(username=f'@{lastNme}', is_staff=True,first_name=firstNme, last_name=lastNme, email=email, password=password)            
            user.set_password(user_form.cleaned_data['password'])                             
            user.save()   
            user.groups.add(Group.objects.get(name='sales'))
            login(request, user)
            return redirect('authy:tenant_table')
    else:
        user_form = UserRegistrationForm()

    return render(request,"signup/sales_signup.html",{"form":user_form})

def renter(request):    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            firstNme = user_form.cleaned_data.get('firstName')
            lastNme = user_form.cleaned_data.get('lastName')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            user = User.objects.create_user(username=f'@{lastNme}', first_name=firstNme, last_name=lastNme, email=email, password=password)            
            user.set_password(user_form.cleaned_data['password'])                             
            user.save()   
            user.groups.add(Group.objects.get(name='renter'))
            login(request, user)
            return HttpResponse('authenticated successfully acc')
    else:
        user_form = UserRegistrationForm()
    return render(request,"signup/renter_signup.html",{"form":user_form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=f"@{cd['username']}",
                                password=cd['password'])
            if user is not None:
                if user.is_staff or user.is_superuser:
                    if user.is_active:
                        login(request, user)
                        return redirect('authy:tenant_table')
                    else:
                        return HttpResponse('disabled acc')
                else:
                    if user.is_active:
                        login(request, user)
                        return HttpResponse('authenticated successfully acc')
                        #return redirect('authy:tenant_table')
                    else:
                        return HttpResponse('disabled acc')
            else:
                return HttpResponse('ivalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

class RenterInfoTableView(ExportMixin,LoginRequiredMixin, UserPassesTestMixin, SingleTableMixin, FilterView):
    table_class = RenterInfoTable
    queryset = RenterInfo.objects.filter(Q(payments__isnull=False)&Q(payments__active=True))
    filterset_class = RenterPaymentUniversalFilter  
     
    paginate_by = 10
    
    
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tenantsInfo/tenantsInfo_htmx_table.html"
        else:
            template_name = "tenantsInfo/tenantsInfo_table.html"
        return template_name
      
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser    
    

class PaymentLogTableView(ExportMixin,SingleTableView,LoginRequiredMixin, UserPassesTestMixin):
    table_class = PaymentLogTable
    queryset = PaymentLog.objects.all()    
    paginate_by = 10
    def get_template_names(self):
        if self.request.htmx:
            template_name = "tenantsInfo/paymentLogHtmx.html"
        else:            
            template_name = "tenantsInfo/paymentLog.html"
        return template_name

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser    

