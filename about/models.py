from django.db import models

# Create your models here.
class GalleryImage(models.Model):
    SECTION_CHOICES = [
        ('facility', 'Manufacturing Facility'),
        ('products', 'Cable Solutions'),
    ]

    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='about/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.get_section_display()} - {self.title or self.alt_text}"