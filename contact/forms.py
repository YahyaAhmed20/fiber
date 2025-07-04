
from django import forms
from .models import ContactInquiry

class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'inquiry_type', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}),
            'inquiry_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Inquiry Type'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject (e.g., Tray Cable Specifications)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your requirements', 'style': 'height: 160px'}),
        }