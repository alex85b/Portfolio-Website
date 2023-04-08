from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Project
from .forms import CommentForm

# Create your views here.

##################################################################################################
################################ Index Page ######################################################
##################################################################################################


# Old_1 - inactive.
class IndexView_Old1(View):
    def get(self, request):
        latest_projects = Project.objects.all().order_by("-date")[:3]
        projects_skills = [proj.skills.all() for proj in latest_projects]
        display_proj = zip(latest_projects, projects_skills)
        return render(request, "portfolio/index.html", {"projects": display_proj})


# Old_2 - inactive.
class IndexView_Old2(TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        latest_projects = Project.objects.all().order_by("-date")[:3]
        context = super().get_context_data(**kwargs)
        context["projects"] = latest_projects
        return context


# New - Active
class IndexView(ListView):
    template_name = "portfolio/index.html"
    model = Project
    ordering = ["-date"]
    context_object_name = "projects"

    # redefine the query to 'Project'
    def get_queryset(self):
        query = super().get_queryset()
        data = query[:3]  # latest 3 --> Only [0, 1, 2]
        return data


##################################################################################################
############################# Project Details Page ###############################################
##################################################################################################


# Old_1 - inactive.
class ProjectDetailsVeiw_Old1(View):
    def get(self, requet, slug):
        print(f"slug: {slug}")
        return render(requet, "portfolio/project_details.html")


# Old_2 - inactive.
class ProjectDetailsVeiw_Old2(TemplateView):
    template_name = "portfolio/project_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_project = get_object_or_404(Project, slug=self.kwargs['slug'])
        context["project"] = target_project
        return context


# Old_3 - inactive.
class ProjectDetailsVeiw_Old3(DetailView):
    template_name = "portfolio/project_details.html"  # who will display the info
    model = Project  # where to find the info
    context_object_name = "project"  # what will be the name of the context object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_members = Project.team_members
        # print(f"team members: {team_members}")
        context["team_members"] = team_members
        context["comment_form"] = CommentForm()
        return context


# New - Active.
class ProjectDetailsVeiw(View):
    template_name = "portfolio/project_details.html"  # who will display the info
    model = Project  # where to find the info
    # context_object_name = "project"  # what will be the name of the context object

    def is_project_saved(self, request, project_id):
        print(f"is_project_saved: project_id={project_id}")
        stored_projects = request.session.get("stored_projects")
        print(f"is_project_saved: stored_projects={stored_projects}")
        if stored_projects is not None:
            if project_id in stored_projects:
                print(f"is_project_saved: project id found in stored")
                return True
        
        print(f"is_project_saved: project id isn't found in stored")
        return False


    def get(self, request, slug):
        project = Project.objects.get(slug=slug)
        context = {
            "project": project,
            "team_members": project.team_members,
            "comment_form": CommentForm(),
            "comments": project.comments.all(),  # type: ignore
            "is_saved": self.is_project_saved(request, project.id) # type: ignore
        }
        return render(request, "portfolio/project_details.html", context)

    def post(self, request, slug):
        # 'bake' a new form out of the post - which contains a form
        comment_form = CommentForm(request.POST)
        project = Project.objects.get(slug=slug)

        if comment_form.is_valid():  # if form has no errors
            # creates a new instance of Form, without saving it
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.save()  # save edited comment to the DB into the Comment table
            return HttpResponseRedirect(
                reverse("project-details", args=[slug])
            )

        context = {
            "project": project,
            "team_members": project.team_members,
            "comment_form": comment_form,  # the form that contains user input !
            "comments": project.comments.all(),  # type: ignore
            "is_saved": self.is_project_saved(request, project.id) # type: ignore
        }
        return render(request, "portfolio/project_details.html", context)


##################################################################################################
################################ All Projects Page ###############################################
##################################################################################################


# New - Active
class AllProjectsView(ListView):
    template_name = "portfolio/all-projects.html"
    model = Project
    context_object_name = "projects"


##################################################################################################
################################ Saved Projects page #############################################
##################################################################################################


# New - Active
class SavedProjectsView(View):

    def get(self, request):

        stored_projects = request.session.get("stored_projects")
        context = {}
        if stored_projects is None or stored_projects == []:
            context["projects"] = []
            context["has_projects"] = False
        else:
            context["projects"] = Project.objects.filter(
                id__in=stored_projects)
            context["has_projects"] = True

        print(f"get -> saved_projects:{stored_projects}")
        return render(request, "portfolio/saved-projects.html", context)

    def post(self, request):
        save_this_project = int(request.POST["project_id"]) # type: ignore
        stored_projects = request.session.get("stored_projects")

        print(f"post -> save this: {save_this_project}")
        print(
            f"post -> session['stored_projects'] has this: {stored_projects}")

        if stored_projects is None:
            stored_projects = []

        if save_this_project not in stored_projects:
            stored_projects.append(save_this_project)
        else:
            stored_projects.remove(save_this_project)

        request.session["stored_projects"] = stored_projects

        print(request.session.get("stored_projects"))
        return HttpResponseRedirect(
            reverse("all-projects")
        )
