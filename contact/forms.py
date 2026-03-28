from django import forms
from django.utils.translation import gettext_lazy as _  # ✅ مهم للترجمة
from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    # ✅ تعريف الحقول بشكل صريح عشان نضيف labels و placeholders قابلة للترجمة
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
    
    inquiry_type = forms.ChoiceField(
        label=_("Inquiry Type"),
        choices=[
            ('', _('Select inquiry type')),  # ✅ الخيار الأول فاضي عشان يختار
            ('quote', _('Request a Quote')),
            ('technical', _('Technical Support')),
            ('partnership', _('Partnership Inquiry')),
            ('general', _('General Inquiry')),
            ('other', _('Other')),
        ],
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
        
    # ✅ تنظيف رقم التليفون (للتحقق من أنه 11 رقم)
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone.replace('+', '').replace('-', '').replace(' ', '')) != 11:
            raise forms.ValidationError(_("Phone number must be exactly 11 digits"))
        return phone