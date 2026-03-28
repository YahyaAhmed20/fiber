from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    # ✅ نعرّف الحقول اللي محتاجين نعدل الـ widget بتاعها بس
    # ✅ حقل inquiry_type هياخد الـ choices أوتوماتيك من المودل
    
    name = forms.CharField(
        label=_("Your Name"),
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your full name'),
            'id': 'name',
            'required': True
        })
    )
    
    email = forms.EmailField(
        label=_("Your Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email address'),
            'id': 'email',
            'required': True
        })
    )
    
    phone = forms.CharField(
        label=_("Your Phone"),
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your phone number (e.g., 01012345678)'),
            'id': 'phone',
            'required': True,
            'pattern': '[0-9]{11}',
            'title': _('Phone number must be 11 digits')
        })
    )
    
    # ✅ حقل inquiry_type: نسيبه ياخد الخيارات من المودل أوتوماتيك
    # ✅ بس نعدل الـ widget عشان يضيف الـ class والـ ID
    inquiry_type = forms.ChoiceField(
        label=_("Inquiry Type"),
        # ✅ مفيش choices هنا! هتاخد من المودل أوتوماتيك
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'inquiry_type',
            'required': True
        })
    )
    
    subject = forms.CharField(
        label=_("Subject"),
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('e.g., Tray Cable Specifications'),
            'id': 'subject',
            'required': True
        })
    )
    
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Describe your requirements (cable type, quantity, specifications, etc.)'),
            'id': 'message',
            'style': 'height: 160px',
            'required': True,
            'rows': 5
        })
    )

    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'inquiry_type', 'subject', 'message']
        
        # ✅ نضيف الخيار الفاضي يدوياً عشان يظهر أول حاجة في الـ dropdown
        # (ده هيشتغل مع الـ widget فوق)
        
    # ✅ دالة لتعديل الـ queryset أو الخيارات بعد التحميل (اختياري)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ نضيف خيار "اختر نوع الاستفسار" كأول عنصر
        self.fields['inquiry_type'].choices = [
            ('', _('Select inquiry type')),
        ] + list(ContactInquiry.INQUIRY_TYPES)
        
    # ✅ تنظيف رقم التليفون (للتحقق من أنه 11 رقم)
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone.replace('+', '').replace('-', '').replace(' ', '')) != 11:
            raise forms.ValidationError(_("Phone number must be exactly 11 digits"))
        return phone