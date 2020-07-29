from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAddress, BillingAddress
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
    address2 = forms.CharField(required=False)
    firstname = forms.CharField(label="First Name")
    lastname = forms.CharField(label="Last Name")
    billing = forms.BooleanField(label="Make this you billing address?",required=False)
    class Meta:
        model = UserAddress
        fields = ['firstname','lastname','address','address2','city','state','country', 'zipcode', 'phone','billing']
        widgets = {
            'firstname': forms.TextInput(attrs = {'placeholder': 'Username'}),
            'password': forms.TextInput(attrs = {'placeholder': 'Password'}),
        }


User = get_user_model()

class BillingAddressForm(forms.ModelForm):
    default = forms.BooleanField(label="Make this your default Address?",required=False)
    address2 = forms.CharField(required=False)
    firstname = forms.CharField(label="First Name")
    lastname = forms.CharField(label="Last Name")
    class Meta:
        model = BillingAddress
        fields = ['firstname','lastname','address','address2','city','state','country', 'zipcode', 'phone','default']
        widgets = {
            'firstname': forms.TextInput(attrs = {'placeholder': 'Username'}),
            'password': forms.TextInput(attrs = {'placeholder': 'Password'}),
        }



User = get_user_model()

class LoginForms(forms.Form):
    username = forms.CharField(label='email address')
    password = forms.CharField(widget=forms.PasswordInput())
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
    username= forms.EmailField(label="Email Address")
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','email']
        widgets = {
            'password1': forms.TextInput(attrs = {'placeholder': 'Password'}),
            'password2': forms.TextInput(attrs = {'placeholder': 'Confirm Password'}),
            'email': forms.HiddenInput()

        }


    def clean_email(self):
        email= self.cleaned_data.get("email")
        print(email)
        user_count= User.objects.filter(email=email).count()
        print(user_count)
        if user_count > 25:
            raise forms.ValidationError("This email has already been used")
        return email



    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'The Username and Password did Not Match'
        self.error_messages['password_mismatch'] = 'The Two Passwords Do Not Match or Your password is to similar '
        super().__init__(*args, **kwargs)


class StripeForm(forms.Form):
    stripeToken = forms.CharField(max_length=80)
    stripeBillingName = forms.CharField(max_length=80, required=False)
    stripeBillingAddressLine1 = forms.CharField(max_length=80, required=False)
    stripeBillingAddressZip = forms.CharField(max_length=80, required=False)
    stripeBillingAddressState = forms.CharField(max_length=80, required=False)
    stripeBillingAddressCity = forms.CharField(max_length=80, required=False)
    stripeBillingAddressCountry = forms.CharField(max_length=80, required=False)

