from django.shortcuts import render
from .models import ExploreSection

# Create your views here.
def home(request):
    sections = ExploreSection.objects.filter(display=True)

    context = {
        'sections': sections,
    }
    
    return render(request, 'base/home.html', context)


