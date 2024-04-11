from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

from portfolio import views

router = routers.DefaultRouter()
router.register('projects', views.ProjectViewSet, basename='project')
router.register('images', views.ImageViewSet, basename='image')
router.register('reviews', views.ReviewViewSet, basename='review')
router.register('offers', views.OfferViewSet, basename='offer')
router.register('accounts', views.ProjectViewSet, basename='user')
router.register('offer-categories', views.OfferCategoryViewSet, basename='offer-category')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', authtoken_views.obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
