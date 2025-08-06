from django.shortcuts import render
from .models import Partner

# Create your views here.




def ourpartner(request):
    partners = Partner.objects.all()
    return render(request, 'ourpartner/ourpartner.html', {
        'partners': partners,
        'active_page': 'ourpartner'
    })

