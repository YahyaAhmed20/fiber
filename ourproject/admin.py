# projects/admin.py

from django.contrib import admin
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [ProjectImageInline]

admin.site.register(Project, ProjectAdmin)
