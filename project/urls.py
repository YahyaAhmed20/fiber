from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import robots_txt
from django.contrib.sitemaps.views import sitemap

# موديلات
from about.models import GalleryImage
from certificates.models import Certificate
from ourpartner.models import Partner
from ourproject.models import Project

# السايت ماب
from .sitemaps import StaticViewSitemap, ModelSitemap

sitemaps_dict = {
    'static': StaticViewSitemap,
    'gallery': ModelSitemap(GalleryImage, changefreq="yearly", priority=0.6),
    'certificates': ModelSitemap(Certificate, changefreq="yearly", priority=0.7),
    'partners': ModelSitemap(Partner, changefreq="yearly", priority=0.5),
    'projects': ModelSitemap(Project, changefreq="monthly", priority=0.9, date_field="created_at"),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('contact-us/', include('contact.urls', namespace='contact')),
    path('about/', include('about.urls', namespace='about')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
    path('ourproject/', include('ourproject.urls', namespace='ourproject')),
    path('ourpartner/', include('ourpartner.urls', namespace='ourpartner')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict}, name='django.contrib.sitemaps.views.sitemap'),

    # Robots.txt
    path("robots.txt", robots_txt, name="robots_txt"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
