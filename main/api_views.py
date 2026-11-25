from django.contrib.auth.models import User
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Education, Project
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly
from main.serializers import EducationSerializer, ProjectSerializer


def _list_with_star_data(queryset, user):
    """Annotate star counts and prefetch only the current user's stars."""
    queryset = queryset.annotate(star_count_value=Count("starred_by", distinct=True))
    if user is not None and user.is_authenticated:
        queryset = queryset.prefetch_related(
            Prefetch("starred_by", queryset=User.objects.filter(pk=user.pk), to_attr="_starred_users")
        )
    return queryset


def _is_starred(obj, user):
    if user is None or not user.is_authenticated:
        return False
    return bool(getattr(obj, "_starred_users", None))


# ==============================================================================
# Education API Endpoints (Individual Assignment 6)
# ==============================================================================


@api_view(["GET", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    """
    GET: Mengembalikan daftar data pendidikan, mendukung filter query '?institution='.
    POST: Menambahkan data pendidikan baru (hanya untuk superuser/pemilik portofolio).
    """
    if request.method == "GET":
        institution_query = request.query_params.get("institution", "").strip()
        education_list = _list_with_star_data(
            Education.objects.order_by("-started_at"), request.user
        )
        if institution_query:
            education_list = education_list.filter(institution__icontains=institution_query)
        serializer = EducationSerializer(education_list, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = EducationSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        education = serializer.save()
        return Response(
            EducationSerializer(education, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    """
    GET: Mengambil detail satu data pendidikan.
    PUT/PATCH: Memperbarui data pendidikan (hanya untuk superuser & editor).
    DELETE: Menghapus data pendidikan (hanya untuk superuser/pemilik).
    """
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "GET":
        return Response(EducationSerializer(education, context={"request": request}).data)

    if request.method in ("PUT", "PATCH"):
        serializer = EducationSerializer(
            education,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    education.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    """
    POST: Memberikan atau membatalkan star pada data pendidikan tertentu.
    Hanya dapat diakses oleh pengguna yang sudah terautentikasi.
    """
    education = get_object_or_404(Education, pk=education_id)
    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)
    education = _list_with_star_data(Education.objects.filter(pk=education.pk), request.user).get()
    return Response(EducationSerializer(education, context={"request": request}).data)


# ==============================================================================
# Project API Endpoints (Tutorial 07)
# ==============================================================================


@api_view(["GET", "POST"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    """
    GET: Mengembalikan daftar data proyek, mendukung filter query '?title='.
    POST: Menambahkan proyek baru (hanya untuk superuser/pemilik portofolio).
    """
    if request.method == "GET":
        title_query = request.query_params.get("title", "").strip()
        projects = _list_with_star_data(
            Project.objects.order_by("-id"), request.user
        )
        if title_query:
            projects = projects.filter(title__icontains=title_query)
        serializer = ProjectSerializer(projects, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        project = serializer.save()
        return Response(
            ProjectSerializer(project, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    """
    GET: Mengambil detail satu data proyek.
    PUT/PATCH: Memperbarui data proyek (hanya superuser).
    DELETE: Menghapus data proyek (hanya superuser).
    """
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "GET":
        return Response(ProjectSerializer(project, context={"request": request}).data)

    if request.method in ("PUT", "PATCH"):
        serializer = ProjectSerializer(
            project,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    """
    POST: Memberikan atau membatalkan star pada proyek.
    Hanya dapat diakses oleh pengguna yang sudah terautentikasi.
    """
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    project = _list_with_star_data(Project.objects.filter(pk=project.pk), request.user).get()
    return Response(ProjectSerializer(project, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """Revoke the token used for the current request."""
    if request.auth is not None:
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
