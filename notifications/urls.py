from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('activity/', views.activity_feed, name='activity_feed'),
    path('callback/request/', views.request_callback, name='request_callback'),
]