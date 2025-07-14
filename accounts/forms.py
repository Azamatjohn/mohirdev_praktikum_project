from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data



    def save(self):
        user = User.objects.create_user(username=self.cleaned_data.get('username'),)
        user.set_password(self.cleaned_data.get('password'))
        user.email = self.cleaned_data.get('email')
        user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birth']






