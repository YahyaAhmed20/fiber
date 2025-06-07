from django.shortcuts import render,redirect


# Create your views here.


def send_text(request):

    return render(request,'contact/contact.html')