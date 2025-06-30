from django.db import models

# Create your models here.


# models.py

class LadderPrice(models.Model):
    type = models.CharField(max_length=50)
    thickness = models.FloatField()
    side = models.FloatField()
    dim = models.FloatField()
    price_final = models.FloatField()

    def __str__(self):
        return f"{self.type} - {self.thickness} - {self.side} - {self.dim}"


class TrayPrice(models.Model):
    type = models.CharField(max_length=50)
    thickness = models.FloatField()
    dim = models.FloatField()
    price_with_joints = models.FloatField()

    def __str__(self):
        return f"{self.type} - {self.thickness} - {self.dim}"
