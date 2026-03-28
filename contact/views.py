from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _  # ✅ مهم للترجمة
from .forms import ContactInquiryForm


def send_text(request):
    """
    Handle contact inquiry form submission
    """
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            # ✅ رسالة النجاح قابلة للترجمة
            messages.success(
                request, 
                _("Thank you! Your inquiry has been submitted successfully. Our team will contact you soon.")
            )
            return redirect('contact:send_text')
        else:
            # ✅ رسالة الخطأ قابلة للترجمة
            messages.error(
                request, 
                _("Please correct the errors below and try again.")
            )
    else:
        form = ContactInquiryForm()

    return render(request, 'contact/contact.html', {
        'active_page': 'contact',
        'form': form
    })