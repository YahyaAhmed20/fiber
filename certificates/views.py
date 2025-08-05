from django.shortcuts import render
from .models import Certificate

# Create your views here.

def certificates(request):
    certificates = Certificate.objects.all()
    return render(request, 'certificates/certificates.html', {
        'certificates': certificates,
        'active_page': 'certificates'
    })