from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import robots_txt
from django.contrib.sitemaps.views import sitemap

# موديلات



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('contact-us/', include('contact.urls', namespace='contact')),
    path('about/', include('about.urls', namespace='about')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
    path('ourproject/', include('ourproject.urls', namespace='ourproject')),
    path('ourpartner/', include('ourpartner.urls', namespace='ourpartner')),

    # Sitemap

    # Robots.txt
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
