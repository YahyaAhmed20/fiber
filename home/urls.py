from django.urls import path
from . import views
from .views import *

# calculate_tray_manual

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    # path('calculate_tray_manual/', calculate_tray_manual, name='calculate_tray_manual'),


    path("calculate_manual_combined/", views.calculate_manual_combined, name="calculate_manual_combined"),

    # path('calculate/', views.calculate_dynamic_price, name='calculate_price'),

]
