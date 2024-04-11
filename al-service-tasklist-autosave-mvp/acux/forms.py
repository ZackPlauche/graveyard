from django.forms import ModelForm, modelformset_factory, modelform_factory

from .models import Service, Task




class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'platform_version']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'completed', 'provisioner_2', 'service']