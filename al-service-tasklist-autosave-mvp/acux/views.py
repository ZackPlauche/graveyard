import json

from django.shortcuts import render, get_object_or_404

from .models import Service, Task
from .forms import ServiceForm


def service_list(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = ServiceForm()
    services = Service.objects.all()
    context = {
        'services': services,
        'form': form,
    }
    return render(request, 'acux/service_list.html', context)


def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    context = {
        'service': service,
    }
    return render(request, 'acux/service_detail.html', context)


@require_POST
def create_or_udpate_task(request):
    data = json.loads(request.body)
    if data['task_id']:
        task = get_object_or_404(Task, pk=data['task_id'])