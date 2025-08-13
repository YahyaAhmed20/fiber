from django.contrib import admin
from .models import Review


    
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'rating', 'order')
    list_editable = ('rating', 'order')
    


from .models import UserData

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'phone', 'email', 'created_at')
    search_fields = ('name', 'company', 'phone', 'email')
    list_filter = ('created_at',)