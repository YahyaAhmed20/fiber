from django.db import models
from django.urls import reverse

class Certificate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='certificates/')
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse("certificates:certificates")