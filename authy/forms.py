from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'input input-bordered w-full','placeholder':'password'}))
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'input input-bordered w-full','placeholder':'confirm password'}))
    firstName = forms.CharField(widget=forms.TextInput(attrs={'class':'input input-bordered max-w-min w-full','placeholder':'first name'}),max_length=45, required=True)    
    lastName = forms.CharField(widget=forms.TextInput(attrs={'class':'input input-bordered max-w-min w-full','placeholder':'last name'}),max_length=45, required=True)    
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'input input-bordered w-full','placeholder':'email'}))
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords don\'t match')
        return cd['password2']
    
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input input-bordered max-w-min w-full','placeholder':'lastname you registered'}),max_length=45, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input input-bordered max-w-min w-full','placeholder':'password'}), required=True)