from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactInquiryForm

def send_text(request):
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been submitted successfully! Our team will contact you soon.')
            return redirect('contact:send_text')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactInquiryForm()

    return render(request, 'contact/contact.html', {
        'active_page': 'contact',
        'form': form
    })