from django.urls import path
from .import views

urlpatterns = [
    path("", views.Index, name="Index"),
    path('project/', views.ProjectPage, name="ProjectPage"),
    path("project-details/<slug:slug>", views.ProjectDetails, name="ProjectDetails"),
    path("contact", views.Contact, name="Contact"),
]
