from django.db import models

# Create your models here.


class Partner(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class PartnerImage(models.Model):
    partner = models.ForeignKey(Partner, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='partner_images/')

    def __str__(self):
        return f"Image for {self.partner.name}"
