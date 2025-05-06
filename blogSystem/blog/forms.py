from django import forms
from .models import BlogPost
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'tags']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)  # Add email field

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include email in fields

    error_messages = {
        'password1': {
            'too_similar': "Your password can’t be too similar to your other personal information.",
            'password_too_common': "Your password can’t be a commonly used password.",
            'password_numeric': "Your password can’t be entirely numeric.",
            'password_length': "Your password must contain at least 8 characters.",
        },
    }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError(self.error_messages['password1']['password_length'])

        if password1.isnumeric():
            raise forms.ValidationError(self.error_messages['password1']['password_numeric'])

        return password1


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Include email in fields

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
