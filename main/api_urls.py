from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    # Individual Assignment 6 (Education)
    path("education/", api_views.education_list, name="education_list"),
    path("education/<uuid:education_id>/", api_views.education_detail, name="education_detail"),
    path("education/<uuid:education_id>/star/", api_views.education_star, name="education_star"),
    # Tutorial 07 (Project)
    path("projects/", api_views.project_list, name="project_list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project_detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project_star"),
]
