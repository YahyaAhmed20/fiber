from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    # ✅ عرض البيانات في القائمة
    list_display = ['name', 'email', 'phone', 'inquiry_type', 'subject', 'created_at', 'is_read']
    
    # ✅ فلاتر جانبية للبحث السريع
    list_filter = ['inquiry_type', 'created_at', 'is_read']
    
    # ✅ حقول البحث
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    
    # ✅ الحقول اللي مش قابلة للتعديل
    readonly_fields = ['created_at', 'is_read']
    
    # ✅ ترتيب البيانات (الأحدث أولاً)
    ordering = ['-created_at']
    
    # ✅ عدد العناصر في الصفحة الواحدة
    list_per_page = 20
    
    # ✅ تنسيق التاريخ
    date_hierarchy = 'created_at'
    
    # ✅ تجميع الحقول في أقسام
    fieldsets = (
        (_("Contact Information"), {
            'description': _("Customer contact details"),
            'fields': ('name', 'email', 'phone')
        }),
        (_("Inquiry Details"), {
            'description': _("Details about the customer inquiry"),
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        (_("System Information"), {
            'description': _("Automatically generated information"),
            'fields': ('created_at', 'is_read'),
            'classes': ('collapse',)  # ✅ قسم قابل للطي
        }),
    )
    
    # ✅ أعمدة قابلة للتعديل من القائمة مباشرة
    list_editable = ['is_read']
    
    # ✅ تخصيص عرض الحقول
    def is_read(self, obj):
        """✅ عرض حالة القراءة"""
        return obj.is_read
    is_read.boolean = True
    is_read.short_description = _("Read Status")
    
    # ✅ تخصيص عنوان الصفحة
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['subtitle'] = _("Manage all contact inquiries")
        return super().changelist_view(request, extra_context=extra_context)
    
    # ✅ منع التعديل على الاستفسارات القديمة (اختياري)
    def has_change_permission(self, request, obj=None):
        # ✅ السماح بالتعديل فقط في أول 7 أيام
        if obj and obj.created_at:
            from django.utils import timezone
            from datetime import timedelta
            if timezone.now() - obj.created_at > timedelta(days=7):
                return False
        return True
    
    # ✅ تخصيص رسالة عند الحذف
    def delete_model(self, request, obj):
        from django.contrib import messages
        messages.warning(
            request, 
            _("Inquiry from {name} has been deleted.").format(name=obj.name)
        )
        super().delete_model(request, obj)