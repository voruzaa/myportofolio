from django.shortcuts import render
from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "Forza Derian",
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

def show_education(request):
    context = {
        "name": "Forza",
        "education_list": Education.objects.all().order_by("-started_at"),
    }
    return render(request, "education.html", context)
