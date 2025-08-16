from django.shortcuts import render, get_object_or_404
from .models import Project

# قائمة المشاريع
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'ourproject/project_list.html', {
        'projects': projects,
        'active_page': 'ourproject'
    })

# تفاصيل مشروع معين
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'ourproject/project_detail.html', {
        'project': project,
        'active_page': 'ourproject'
    })
