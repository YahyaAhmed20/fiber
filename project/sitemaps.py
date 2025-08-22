from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = 'https'  # HTTPS

    def items(self):
        return [
            'home:home',
            'about:about',
            'certificates:certificates',
            'ourpartner:ourpartner',
            'ourproject:project_list',
            'contact:send_text'
        ]

    def location(self, item):
        return reverse(item)  # فقط المسار النسبي بدون الدومين
