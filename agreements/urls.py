from django.urls import path
from . import views

app_name = 'agreements'

urlpatterns = [
    # Sales/Employee URLs
    path('', views.agreement_list, name='agreement_list'),
    path('create/', views.agreement_create, name='agreement_create'),
    path('<int:pk>/', views.agreement_detail, name='agreement_detail'),
    path('<int:pk>/edit/', views.agreement_edit, name='agreement_edit'),
    path('<int:pk>/delete/', views.agreement_delete, name='agreement_delete'),
    path('<int:pk>/pdf/', views.agreement_pdf, name='agreement_pdf'),
    
    # Manager URLs
    path('manager/', views.manager_agreement_list, name='manager_agreement_list'),
    
    # Admin URLs
    path('admin/', views.admin_agreement_list, name='admin_agreement_list'),
]
