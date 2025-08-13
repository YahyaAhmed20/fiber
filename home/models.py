from django.db import models

# Create your models here.



    
class Review(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='reviews/')
    rating = models.PositiveIntegerField(default=5)  # من 1 إلى 5
    comment = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.job_title}"
    



class UserData(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company}"