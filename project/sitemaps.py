from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from about.models import GalleryImage
from certificates.models import Certificate
from ourpartner.models import Partner, PartnerImage
from ourproject.models import Project


class ModelSitemap(Sitemap):
    def __init__(self, model, changefreq="monthly", priority=0.5, date_field=None):
        self.model = model
        self.changefreq = changefreq
        self.priority = priority
        self.date_field = date_field

    def items(self):
        return self.model.objects.all()

    def lastmod(self, obj):
        if self.date_field and hasattr(obj, self.date_field):
            return getattr(obj, self.date_field)
        return None


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            'home:home',
            'about:about',
            'contact:send_text',
            'certificates:certificates',
            'ourpartner:ourpartner',
            'ourproject:ourproject',
        ]

    def location(self, item):
        return reverse(item)


class GalleryImageSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.6

    def items(self):
        return GalleryImage.objects.all()


class CertificateSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.7

    def items(self):
        return Certificate.objects.all()


class PartnerSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Partner.objects.all()


class PartnerImageSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.4

    def items(self):
        return PartnerImage.objects.all()


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return getattr(obj, 'created_at', None)
