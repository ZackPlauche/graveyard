from rest_framework import serializers

from .models import Restaurant, Customer, Ingredient, MenuItem, Menu, Order, Tier


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['url', 'id', 'title', 'items' 'slug']
        depth = 1


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['url', 'id', 'title', 'slug', 'items',  'active', 'created_at', 'last_updated', 'image', 'order']
        depth = 1
        lookup_field = 'slug'
        extra_kwargs = { 'url': {'lookup_field': 'slug'} }


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['url', 'id', 'title', 'description', 'price', 'image', 'active', 'created_at', 'last_updated', 'menu']
