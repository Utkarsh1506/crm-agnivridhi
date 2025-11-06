from django.urls import path
from . import views

urlpatterns = [
    # Application list and detail
    path('', views.application_list, name='application_list'),
    path('pending/', views.pending_applications, name='pending_applications'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('create/<int:scheme_id>/', views.create_application, name='create_application'),
    
    # Manager actions
    path('<int:pk>/approve/', views.approve_application, name='approve_application'),
    path('<int:pk>/reject/', views.reject_application, name='reject_application'),
]
