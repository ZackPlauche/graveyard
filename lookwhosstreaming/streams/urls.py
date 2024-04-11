from django.urls import path
from .views import *

app_name = "streams"

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('top-charts/', TopChart.as_view(), name="top_chart"),
    path('admin/', Admin.as_view(), name="admin"),

    # Streams
    path('admin/streams/', StreamList.as_view(), name="stream_list"),
    path('admin/streams/create', StreamCreate.as_view(), name="stream_create"),
    path('admin/streams/<pk>/', StreamDetail.as_view(), name="stream_detail"),
    path('admin/streams/<pk>/update', StreamUpdate.as_view(), name="stream_update"),
    path('admin/streams/<pk>/delete', StreamDelete.as_view(), name="stream_delete"),


    # Streamers
    path('admin/streamers/', StreamerList.as_view(), name="streamer_list"),
    path('admin/streamers/create', StreamerCreate.as_view(), name="streamer_create"),
    path('admin/streamers/<pk>/', StreamerDetail.as_view(), name="streamer_detail"),
    path('admin/streamers/<pk>/update', StreamerUpdate.as_view(), name="streamer_update"),
    path('admin/streamers/<pk>/delete', StreamerDelete.as_view(), name="streamer_delete"),

    # API Accounts
    path('admin/api-accounts/', APIAccountList.as_view(), name="apiaccount_list"),
    path('admin/api-accounts/create', APIAccountCreate.as_view(), name="apiaccount_create"),
    path('admin/api-accounts/<pk>/', APIAccountDetail.as_view(), name="apiaccount_detail"),
    path('admin/api-accounts/<pk>/update', APIAccountUpdate.as_view(), name="apiaccount_update"),
    path('admin/api-accounts/<pk>/delete', APIAccountDelete.as_view(), name="apiaccount_delete")
]
