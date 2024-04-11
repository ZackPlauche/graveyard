from django.shortcuts import render

from blog.models import BlogPost



def home(request):
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'index.html', context=context)