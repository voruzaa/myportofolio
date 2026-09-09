from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Forza",
        "npm": "2506596041",
        "study_program": "S1 Information Systems",
        "bio": (
            "Information Systems student at Universitas Indonesia with an interest "
            "in software development and education."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Forza",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)