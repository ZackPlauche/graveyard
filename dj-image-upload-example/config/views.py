from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def home(request):
    if request.method == 'POST':
        print(request.FILES)
    return render(request, 'index.html')