from django.contrib import admin
from .models import TeamMember,Review

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'rating', 'order')
    list_editable = ('rating', 'order')
    
