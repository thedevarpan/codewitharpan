from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from myblog.models import Blog, Tag, Author, BlogCategory
from.models import *


# Create your views here.
def Index(request):
    all_posts = Blog.objects.all().order_by('-id')[:2] 
    all_tags = Tag.objects.all()
    print(all_posts)
    params = {'all_posts': all_posts, 'all_tags': all_tags}
    return render(request, 'arpan/index.html', params)


def ProjectPage(request):
    all_projects = Project.objects.all()
    print(all_projects)
    params = {
        'all_projects': all_projects
    }
    return render(request, 'arpan/project-page.html', params)



def ProjectDetails(request, slug):
    get_projects = Project.objects.get(slug=slug)
    all_projects = Project.objects.all().order_by('-id')


    # Get all blogs ordered by their creation date
    filtered_project = Project.objects.order_by('created_at')
    project_index = list(filtered_project).index(get_projects)
    # Determine previous and next blogs
    prev_project = filtered_project[project_index - 1] if project_index > 0 else None
    next_project = filtered_project[project_index + 1] if project_index < len(filtered_project) - 1 else None


    params = {
        'get_projects': get_projects,
        'all_projects': all_projects,
        'prev_project': prev_project,
        'next_project': next_project,
        'filtered_project': filtered_project,
        'project_index': project_index,
    }
    return render(request, 'arpan/project-details.html', params)


def Contact(request):
    return HttpResponse("Contact")