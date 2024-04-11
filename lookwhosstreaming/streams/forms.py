from django import forms
from .models import *


# Custom Fields

class AccountModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_with_platform


# Forms
class AddScheduleForm(forms.Form):
    schedule = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv, .xlsx'}), label="Upload File")
    
class BulkAddStreamersForm(forms.Form):
    schedule = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv, .xlsx'}), label="Upload File")

class StreamForm(forms.ModelForm): 
    host = AccountModelChoiceField(queryset=Account.objects.all().order_by('streamer'))
    start_time = forms.DateTimeField(input_formats=["%m/%d/%Y %I:%M%p"], widget=forms.widgets.DateTimeInput(attrs={'placeholder': "Example: 1/29/2020 10:00pm"}))

    class Meta:
        model = Stream
        fields = ['host', 'broadcast_id', 'url', 'start_time']

class StreamerForm(forms.Form):
    streamer_name = forms.CharField(max_length=50)
    instagram_username = forms.CharField(max_length=50, required=False)
    twitch_username = forms.CharField(max_length=50, required=False)
    youtube_username = forms.CharField(max_length=50, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)


class APIAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta: 
        model = APIAccount
        fields = '__all__'
