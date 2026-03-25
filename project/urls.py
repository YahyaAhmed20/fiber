from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from home.views import robots_txt
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.views.static import serve

# 🔥 مهم
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 لتغيير اللغة
    path('i18n/', include('django.conf.urls.i18n')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap}}, name='django.contrib.sitemaps.views.sitemap'),

    # Robots.txt
    path('robots.txt', robots_txt, name='robots'),
]

# 🔥 كل الصفحات اللي عايزها تدعم تعدد اللغات
urlpatterns += i18n_patterns(
    path('', include('home.urls', namespace='home')),
    path('contact-us/', include('contact.urls', namespace='contact')),
    path('about/', include('about.urls', namespace='about')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
    path('ourproject/', include('ourproject.urls', namespace='ourproject')),
    path('ourpartner/', include('ourpartner.urls', namespace='ourpartner')),
    prefix_default_language=False  # 🔥 دي المهمة
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)