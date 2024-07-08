import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import password_validators_help_text_html

from .models import User, Profile


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        strip=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0 border-bottom rounded-0',
            'id': 'username',
            'placeholder': 'Имя пользователя',
            'maxlength': '20'
        })
    )
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control border-0 border-bottom rounded-0',
        'id': 'email',
        'placeholder': 'name@example.com'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control border-0 border-bottom rounded-0',
            'id': 'password1',
            'placeholder': 'password1'
        }),
        help_text=password_validators_help_text_html()
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control border-0 border-bottom rounded-0',
            'id': 'password2',
            'placeholder': 'password2'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control border-0 border-bottom rounded-0',
        'id': 'password',
        'placeholder': 'Password'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control border-0 border-bottom rounded-0',
        'id': 'email',
        'placeholder': 'name@example.com'
    }))

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Password'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.filter(email=email).first()
        print(user.check_password(password))
        if (not user) or (not user.check_password(password)):
            raise forms.ValidationError('Email or password is wrong')

        return self.cleaned_data


class BaseUpdateForm(forms.ModelForm):

    def is_valid(self, *args, **kwargs):
        result = super().is_valid()
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' ' + 'is-invalid'})
        return result


class UserUpdateForm(BaseUpdateForm):

    def clean_username(self):
        username = self.cleaned_data['username']

        if not username:
            raise forms.ValidationError('The user name cannot be empty')

        match = re.match('^[a-zA-Z0-9_]+$', username)

        if match is None:
            error_string = 'The username contains invalid characters. Only "a-z, A-Z, 0-9, _" is available.'
            raise forms.ValidationError(error_string)

        return username

    class Meta:
        model = User
        fields = ['username', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'textinput textInput form-control'})
        }


class ProfileUpdateForm(BaseUpdateForm):
    status = forms.Textarea()

    class Meta:
        model = Profile
        fields = ['status', 'sex', 'birthday', 'first_name', 'last_name']
        widgets = {
            'status': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
            'sex': forms.Select(attrs={'class': 'select form-control'}),
            'birthday': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
        }