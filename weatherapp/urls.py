from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<city_name>/', views.dcity, name='delete_city'),
]
