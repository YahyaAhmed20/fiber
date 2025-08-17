from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import robots_txt
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap  # استيراد الـ sitemap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('contact-us/', include('contact.urls', namespace='contact')),
    path('about/', include('about.urls', namespace='about')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
    path('ourproject/', include('ourproject.urls', namespace='ourproject')),
    path('ourpartner/', include('ourpartner.urls', namespace='ourpartner')),
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
    # Robots.txt
    path('robots.txt', robots_txt, name='robots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)