from django.urls import path
from . import views

# Namespace for reverse() calls like 'schemes:scheme_detail'
app_name = 'schemes'

urlpatterns = [
    # Scheme list and detail
    path('', views.scheme_list, name='scheme_list'),
    path('<int:pk>/', views.scheme_detail, name='scheme_detail'),
    path('check-eligibility/', views.check_eligibility, name='check_eligibility'),
]
