from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Education, Project
from main.forms import EducationForm, ProjectForm


def show_main(request):
    context = {
        "name": "Forza",
        "npm": "2506596041",
        "study_program": "S1 Information Systems",
        "bio": "Undergraduate Information Systems Student at Faculty of Computer Science, Universitas Indonesia.",
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
    }
    return render(request, "education.html", context)


def create_education(request):
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


def update_education(request, education_id):
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


def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Data pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


# ──────────────────────────────────────────────
#  Project – JSON, List, Create, Delete
# ──────────────────────────────────────────────

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Forza",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)


def create_project(request):
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


def update_project(request, project_id):
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


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")
