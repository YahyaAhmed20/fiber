from django.shortcuts import render
from .models import Project

# Create your views here.


def ourproject(request):
    
    projects = Project.objects.all()

    return render(request, 'ourproject/ourproject.html',{
        
        
        'projects': projects,
        'active_page': 'ourproject'
        
    })




