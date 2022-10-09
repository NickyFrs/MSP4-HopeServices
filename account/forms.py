from django import forms
from django_countries.fields import CountryField
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import UserBase


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Enter Username', min_length=4,
                               max_length=255, help_text='Required', required=True)
    email = forms.EmailField(label='Email', max_length=100,
                             help_text='Required', error_messages={'required': 'Sorry, you need an email address'},
                             required=True)
    password = forms.CharField(label='Password', min_length=4, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', min_length=4, widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('username', 'email')

        # check if the username is already in use.
        def clean_username(self):
            username = self.cleaned_data['username'].lower()
            r = UserBase.objects.filter(username=username)
            if r.count():
                raise forms.ValidationError("Username is already in use")
            return username

        # Confirm that the password entry match. Password validation
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Password do not match.')
            return cd['password2']

        # Confirm that the email exist in DB. Email validation
        def clean_email(self):
            email = self.cleaned_data['email']
            if UserBase.objects.filter(email=email).exists():
                raise forms.ValidationError('Email already in use. Please use another one.')
            return email

        # To add access to the input fields.
        # classes and Bootstrap to the input fields
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'Username'})
            self.fields['email'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
            self.fields['password'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'Password'})
            self.fields['password2'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Username',
               'id': 'login-username'
               }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Password',
               'id': 'login-password'
               }
    ))


class UserEditForm(forms.ModelForm):
    # readonly fields prevent the field to be updated (one way of doing this at least)

    email = forms.EmailField(
        label="Account Email (can't be changed)", max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'form-email', 'readonly': 'readonly'}))

    username = forms.CharField(
        label="Account Username (can't be changed)", max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'
                   }
        ))

    first_name = forms.CharField(
        label="First Name", max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name', 'id': 'form-first-name',
                   }
        ))

    last_name = forms.CharField(
        label="Last Name", max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id': 'form-last-name',
                   }
        ))

    mobile = forms.CharField(
        label="Mobile number", max_length=15, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Mobile number', 'id': 'form-mobile',
                   }
        ))

    address_l1 = forms.CharField(
        label="Address", max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Address', 'id': 'form-address-l1',
                   }
        ))

    address_l2 = forms.CharField(
        label="Address", max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Address', 'id': 'form-address-l2',
                   }
        ))

    city = forms.CharField(
        label="City/County", max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City/County', 'id': 'form-city',
                   }
        ))

    post_code = forms.CharField(
        label="Post Code", max_length=12, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Post Code', 'id': 'form-post-code',
                   }
        ))

    country = CountryField()

    # country = forms.CharField(
    #     label="Country", max_length=12, widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Country', 'id': 'form-country',
    #                }
    #     ))

    class Meta:
        model = UserBase
        fields = ('username', 'email', 'first_name', 'last_name', 'mobile',
                  'address_l1', 'address_l2', 'city', 'post_code', 'country')

        # Confirm that the password entry match. Password validation
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Password do not match.')
            return cd['password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "Looks like that account is not in our system"
            )
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

