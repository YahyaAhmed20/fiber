from django.urls import path
from . import views
from .views import *

# calculate_tray_manual

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    # path('calculate_tray_manual/', calculate_tray_manual, name='calculate_tray_manual'),


    path("calculate_manual_combined/", views.calculate_manual_combined, name="calculate_manual_combined"),
    path('robots.txt', views.robots_txt, name='robots_txt'),

    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),  # ← السطر الجديد

    path('googleb7c44eff2d1899d9.html', views.google_verify, name='google_verify'),   
    # path('calculate/', views.calculate_dynamic_price, name='calculate_price'),

]
