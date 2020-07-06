from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAddress
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     # first_name = forms.CharField(required=True)
#     # last_name = forms.CharField(required=True)
#
#     class Meta:
#         model = User
#         fields = ['username','email','password1','password2']
# fields = ['username','first_name','last_name','email','password1','password2']
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)


class UserAddressForm(forms.ModelForm):
    default= forms.BooleanField(label="Make this your default Address?",required=False)
    class Meta:
        model = UserAddress
        fields = ['address','address2','city','state','country', 'zipcode', 'phone','billing']

User = get_user_model()

class LoginForms(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Password'}))
    widgets = {
        'username': forms.TextInput(attrs = {'placeholder': 'Username'}),
        'password': forms.TextInput(attrs = {'placeholder': 'Password'}),
    }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except  User.DoesNotExist:
            raise forms.ValidationError("User Does Not Exist")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError("Please check your password again.")
        elif user is None:
            pass
        else:
            return password




class CreateUserForm(UserCreationForm):
    email= forms.EmailField(widget = forms.TextInput(attrs={'placeholder': 'E-Mail'}))
    username = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Confirm Password'}))
    first_name = forms.CharField(max_length=30, required=False, widget = forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=False, widget = forms.TextInput(attrs={'placeholder': 'Last Name'}))
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password1', 'password2']
        password1= forms.CharField(label="Password")
        widgets = {
            'username': forms.TextInput(attrs = {'placeholder': 'Username'}),
            'email': forms.TextInput(attrs = {'placeholder': 'E-Mail'}),
            'password1': forms.TextInput(attrs = {'placeholder': 'Password'}),
            'password2': forms.TextInput(attrs = {'placeholder': 'Confirm Password'}),
            'first_name': forms.TextInput(attrs= {'placeholder' : 'First Name'}),
        }

    def clean_email(self):
        email= self.cleaned_data.get("email")
        user_count= User.objects.filter(email=email).count()
        print(user_count)
        if user_count > 0:
            raise forms.ValidationError("This email has already been used")
        return email


class StripeForm(forms.Form):
    stripeToken = forms.CharField(max_length=80)
    stripeBillingName = forms.CharField(max_length=80, required=False)
    stripeBillingAddressLine1 = forms.CharField(max_length=80, required=False)
    stripeBillingAddressZip = forms.CharField(max_length=80, required=False)
    stripeBillingAddressState = forms.CharField(max_length=80, required=False)
    stripeBillingAddressCity = forms.CharField(max_length=80, required=False)
    stripeBillingAddressCountry = forms.CharField(max_length=80, required=False)

