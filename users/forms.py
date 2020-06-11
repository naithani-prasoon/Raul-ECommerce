from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAddress
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
    default= forms.BooleanField(label="Make Default")
    class Meta:
        model = UserAddress
        fields = ['address','address2','city','state','country', 'zipcode', 'phone']


class CreateUserForm(UserCreationForm):
    email= forms.EmailField(label="Email")
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        password1= forms.CharField(label="Password")
        widgets = {
            'username': forms.TextInput(attrs = {'placeholder': 'Username'}),
            'email': forms.TextInput(attrs = {'placeholder': 'E-Mail'}),
            'password1': forms.TextInput(attrs = {'placeholder': 'Password'}),
            'password2': forms.TextInput(attrs = {'placeholder': 'Confirm Password'}),
        }

    def clean_email(self):
        email= self.cleaned_data.get("email")
        user_count= User.objects.filter(email=email).count()
        print(user_count)
        if user_count > 0:
            raise forms.ValidationError("This email has already been used")
        return email