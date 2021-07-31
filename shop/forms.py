from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from django.contrib.auth.models import User

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'product_name' : forms.TextInput(attrs={'style': 'width: 300px;', 'class': 'form-control'}),
            'category' : forms.TextInput(attrs={'style': 'width: 300px;', 'class': 'form-control'}),
            'subcategory' : forms.TextInput(attrs={'style': 'width: 300px;', 'class': 'form-control'}),
            'price' : forms.NumberInput(attrs={'style': 'width: 300px;', 'class': 'form-control'}),
            'desc' : forms.Textarea(attrs={'style': 'width: 300px;', 'class': 'form-control'}),
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
        # widgets = {
        #     'username' : forms.TextInput(attrs={'style': 'width: 300px;', 'class': 'form-control', "placeholder":"Enter Username"}),
        #     'email' : forms.TextInput(attrs={'style': 'width: 300px;', 'class': 'form-control',"placeholder":"Enter Email", 'type':'email'}),
        #     'password1' : forms.PasswordInput(attrs={'style': 'width: 300px;', 'class': 'form-control',"placeholder":"Enter Password"})
        # }

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

# class UserRegisterForm(forms.ModelForm):
#     username = forms.CharField(label=_('username'),
#                                 error_messages={'required': _('Username is Required'),
#                                                 'invalid': _('This value must contain only letters, numbers and underscores.')}, required=True,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
#                                error_messages={'required': _('Password is Required'),
#                                                'invalid': _('This value must contain only letters, numbers and underscores.')})
#     password1 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
#                                        error_messages={'required': _('Confirm Password is Required'),
#                                                        'invalid': _('This value must contain only letters, numbers and underscores.')})
#     email = forms.CharField(label=_('Email'), required=True,
#                            error_messages={'required': _('Email is Required'),
#                                            'invalid': _('This value must contain email type')},
#                            widget=forms.TextInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ('username', 'password','password1','email')


#     def clean_email(self):
#         # Get the email
#         email = self.cleaned_data.get('email')

#         # Check to see if any users already exist with this email as a username.
#         try:
#             match = User.objects.get(email=email)
#         except User.DoesNotExist:
#             # Unable to find a user, this is fine
#             return email

#         # A user was found with this as a username, raise an error.
#         raise forms.ValidationError('This email address is already in use.')