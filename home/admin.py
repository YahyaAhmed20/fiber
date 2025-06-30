# admin.py
from django.contrib import admin
from .models import LadderPrice, TrayPrice

@admin.register(LadderPrice)
class LadderAdmin(admin.ModelAdmin):
    list_display = ['type', 'thickness', 'side', 'dim', 'price_final']
    list_filter = ['type']
    search_fields = ['type']

@admin.register(TrayPrice)
class TrayAdmin(admin.ModelAdmin):
    list_display = ['type', 'thickness', 'dim', 'price_with_joints']
    list_filter = ['type']
    search_fields = ['type']
