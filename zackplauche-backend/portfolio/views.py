from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets

from .serializers import ImageSerializer, ProjectSerializer, ReviewSerializer, OfferSerializer, OfferCategorySerializer
from .models import Project, Image, Review, Offer, OfferCategory


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_fields = '__all__'

    @method_decorator(cache_page(600))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class OfferViewSet(viewsets.ModelViewSet):
   queryset = Offer.objects.all()
   serializer_class = OfferSerializer


class OfferCategoryViewSet(viewsets.ModelViewSet):
   queryset = OfferCategory.objects.all()
   serializer_class = OfferCategorySerializer