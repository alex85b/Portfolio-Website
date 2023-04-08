from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="main-page"),
    path("projects", views.AllProjectsView.as_view(), name="all-projects"),
    path("<slug:slug>", views.ProjectDetailsVeiw.as_view(), name="project-details"),
    path("saved/", views.SavedProjectsView.as_view(), name="saved-projects")
]