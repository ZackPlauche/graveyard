from django import forms
from django.contrib.auth import get_user_model

class ContactForm(forms.ModelForm):
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'message')

    def save(self, commit=True):
        user = super().save(commit=False)
        message = self.cleaned_data['message']
        if commit:
            user.save()
            user.messages.create(message=message)
        return user

