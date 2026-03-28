from django.db import models
from django.utils.translation import gettext_lazy as _  # ✅ مهم للترجمة


class ContactInquiry(models.Model):
    # ✅ ترجمة خيارات inquiry_type
    INQUIRY_TYPES = [
        ('quote', _('Request a Quote')),
        ('technical', _('Technical Support')),
        ('custom', _('Custom Cable Solutions')),
        ('other', _('Other')),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Enter your full name")
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        help_text=_("Enter a valid email address")
    )
    phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name=_("Phone"),
        help_text=_("Enter your phone number (optional)")
    )
    inquiry_type = models.CharField(
        max_length=20, 
        choices=INQUIRY_TYPES,
        verbose_name=_("Inquiry Type"),
        help_text=_("Select the type of your inquiry")
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject"),
        help_text=_("Brief description of your inquiry")
    )
    message = models.TextField(
        verbose_name=_("Message"),
        help_text=_("Describe your requirements in detail")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        editable=False
    )
    # ✅ حقل is_read الجديد
    is_read = models.BooleanField(
        default=False,
        verbose_name=_("Read Status"),
        help_text=_("Mark as read when you review this inquiry"),
        db_index=True  # ✅ تحسين أداء الفلترة
    )

    class Meta:
        verbose_name = _("Contact Inquiry")
        verbose_name_plural = _("Contact Inquiries")
        ordering = ['-created_at']  # ✅ الأحدث أولاً
        indexes = [
            models.Index(fields=['-created_at']),  # ✅ فهرس للترتيب
            models.Index(fields=['is_read', '-created_at']),  # ✅ فهرس للفلترة
        ]

    def __str__(self):
        # ✅ عرض الاسم والموضوع باللغة الحالية
        return f"{self.name} - {self.subject}"
    
    def get_inquiry_type_display_translated(self):
        """✅ دالة مساعدة لعرض نوع الاستفسار مترجم في القوالب"""
        return self.get_inquiry_type_display()
    
    def mark_as_read(self):
        """✅ دالة لتمييز الاستفسار كمقروء"""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    def mark_as_unread(self):
        """✅ دالة لتمييز الاستفسار كغير مقروء"""
        self.is_read = False
        self.save(update_fields=['is_read'])
    
    @property
    def is_new(self):
        """✅ خاصية للتحقق لو الاستفسار جديد (غير مقروء)"""
        return not self.is_read