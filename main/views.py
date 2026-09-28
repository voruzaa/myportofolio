import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Education, Project
from main.forms import EducationForm, ProjectForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


# ──────────────────────────────────────────────
#  Role helpers
# ──────────────────────────────────────────────

def _is_editor(user):
    """Return True if *user* belongs to the 'Editor' Django Group."""
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


def _role_context(user):
    """Build a dict of boolean flags that templates use to show/hide actions."""
    editor = _is_editor(user)
    return {
        "is_editor": editor,
        "can_create": user.is_superuser,
        "can_edit": user.is_superuser or editor,
        "can_delete": user.is_superuser,
    }


# ──────────────────────────────────────────────
#  Auth – Register / Login / Logout
# ──────────────────────────────────────────────

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Forza",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Forza",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


# ──────────────────────────────────────────────
#  Main / Experience (read-only, no auth needed)
# ──────────────────────────────────────────────

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Forza",
        "npm": "2506596041",
        "study_program": "S1 Information Systems",
        "bio": (
            "Undergraduate Information Systems Student at Faculty of Computer Science, Universitas Indonesia."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Forza",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


# ──────────────────────────────────────────────
#  Education – JSON, List, Create, Update, Delete
# ──────────────────────────────────────────────

def get_education_json(request):
    education = Education.objects.all().order_by("-started_at")
    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")


def show_education(request):
    json_response = get_education_json(request)

    education_deserialized = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [entry.object for entry in education_deserialized]

    context = {
        "name": "Forza",
        "education_list": education_list,
        **_role_context(request.user),
    }
    return render(request, "education.html", context)


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Forza",
        "form": form,
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def update_education(request, education_id):
    if not (request.user.is_superuser or _is_editor(request.user)):
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Forza",
        "form": form,
        "education": education,
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Data pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


# ──────────────────────────────────────────────
#  Project – JSON, List, Create, Update, Delete
# ──────────────────────────────────────────────

def get_projects_json(request):
    """Public JSON endpoint — excludes starred_by to prevent leaking user data."""
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize(
        "json",
        projects,
        fields=["title", "description", "tech_stack", "project_url", "project_image_url"],
    )
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Forza",
        "project_list": projects,
        "title_query": title_query,
        **_role_context(request.user),
    }
    return render(request, "project.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Forza",
        "form": form,
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not (request.user.is_superuser or _is_editor(request.user)):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Forza",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")
