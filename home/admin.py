from django.contrib import admin
from .models import Review


    
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'rating', 'order')
    list_editable = ('rating', 'order')
    
