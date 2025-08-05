from django.urls import path
from . import views
from .views import *

# calculate_tray_manual

app_name = 'certificates'

urlpatterns = [
    path('', views.certificates, name='certificates'),




]
