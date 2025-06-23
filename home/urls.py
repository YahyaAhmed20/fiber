from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate-price/', views.calculate_price, name='calculate_price'),
    
]
