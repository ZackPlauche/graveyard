from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('thank-you/', views.thank_you, name="thank_you"),
    path('faq/', views.faq, name="faq"),
    path('events/', views.events, name="events"),
    path('events/<slug:event_slug>/', views.event_detail, name="event_detail"),
    path('signup/', views.signup, name="signup")
]
