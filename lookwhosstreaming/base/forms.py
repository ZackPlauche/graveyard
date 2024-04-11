from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class CreateAccountForm(UserCreationForm):
    full_name = forms.CharField(label="Your name")
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("full_name", "username", "email", )

    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        first_name, last_name = self.cleaned_data["full_name"].split()
        user.first_name = first_name
        user.last_name = last_name
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


