from .models import HomePage

def menus(request):
    context = {}
    if home_page := HomePage.objects.first():
        context['main_menu'] = home_page.get_children().live().in_menu()
    return context