from django.urls import path
from . import views
from .views import *

# calculate_tray_manual

app_name = 'ourproject'

urlpatterns = [
    path('', views.ourproject, name='ourproject'),




]
