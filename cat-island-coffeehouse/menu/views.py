from django.shortcuts import render
from .models import MenuItem, MenuCategory
from django.utils.text import slugify

# Create your views here.
def menu(request):
    categories = MenuCategory.objects.filter(display=True)
    items = MenuItem.objects.filter(display=True)

    context = {
        'categories': categories,
        'items': items,
    }

    return render(request, 'menu/menu.html', context)

def menu_item_detail(request, menu_item_slug):
    items = MenuItem.objects.filter(display=True)
    
    for item in items:
        if slugify(item.title) == menu_item_slug:
            menu_item = item
            break

    context = {
        'item': menu_item,
    }

    return render(request, 'menu/menu-item-detail.html', context)
