from rest_framework import serializers

from .models import Image, Project, Review, Offer, OfferCategory


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        depth = 2


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        depth = 1


class OfferSerializer(serializers.ModelSerializer):
   
   class Meta:
       model = Offer
       fields = '__all__'
       depth = 1


class OfferCategorySerializer(serializers.ModelSerializer):
   
   class Meta:
       model = OfferCategory
       fields = '__all__'