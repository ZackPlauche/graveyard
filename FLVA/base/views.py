from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .models import Post, Contact, FAQ, AboutSection, Event
from .forms import ContactForm, SignupForm

# Create your views here.
def index(request):
    posts = Post.objects.all()
    events = Event.objects.all()

    context = {
    'posts': posts,
    'events':events,
    }

    return render(request, 'base/index.html', context)

def about(request):
    about_sections = AboutSection.objects.all()
    context = {'about_sections': about_sections}
    return render(request, 'base/about.html', context)

def events(request):
    events = Event.objects.all()

    context = {
        'events': events,
    }

    return render(request, 'base/event-index.html', context)

def event_detail(request, event_slug):

    events = Event.objects.all()

    for event in events:
        if slugify(event.title) == event_slug:
            instance = event
            break

    context = {
        'event': instance,
    }

    return render(request, 'base/event-detail.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        form.save()
        return HttpResponseRedirect('../thank-you/')
    else:
        form = ContactForm
        context = {'form': form}
        return render(request, 'base/contact.html', context)

def faq(request):
    faqs = FAQ.objects.all()
    context = {
        'faqs':  faqs
    }
    return render(request, 'base/faq.html', context)

def thank_you(request):
    return render(request, 'base/thank-you.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        form.save()
        return HttpResponseRedirect('../thank-you/')
    else:
        form = SignupForm()
        context = {'form': form}
        return render(request, 'base/signup.html', context)
