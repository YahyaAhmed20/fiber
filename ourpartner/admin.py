from django.contrib import admin
from .models import Partner, PartnerImage

class PartnerImageInline(admin.TabularInline):
    model = PartnerImage
    extra = 1

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    inlines = [PartnerImageInline]
    list_display = ['name']
