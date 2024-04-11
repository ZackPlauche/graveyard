from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu, name="menu"),
    path('<slug:menu_item_slug>/', views.menu_item_detail, name="menu-item-detail"),
]