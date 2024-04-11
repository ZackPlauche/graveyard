from django.urls import path

from . import views


urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('api/tasks/', views.create_or_update_task, name='create_or_update_task'),
]