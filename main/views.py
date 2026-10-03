from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied 

from main.forms import ProjectForm, EducationForm
from main.models import Experience, Project, Education

import datetime

#helper is_editor
def is_editor(user):
    return user.groups.filter(name="Editor").exists()

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Kevin",
        "npm": "2506621466",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Currently IS student at Universitas Indonesia,"
            "always excited to learn new things and build cool stuffs along the way."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Kevin",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Kevin",
        "title_query": title_query,
        "is_editor": (
            is_editor(request.user)
            if request.user.is_authenticated
            else False
        ),
    }

    return render(request, "projects.html", context)

@login_required(login_url="/login/")
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Kevin",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []

    for project in projects:
        starred_users = list(project.starred_by.all())

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            user.username for user in starred_users
        )

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)

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

def get_education_json(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Metode request tidak didukung."},
            status=405,
        )

    institution_query = request.GET.get("institution", "").strip()
    education_items = Education.objects.prefetch_related("starred_by")

    if institution_query:
        education_items = education_items.filter(
            institution__icontains=institution_query
        )

    data = []

    for item in education_items:
        starred_users = list(item.starred_by.all())

        data.append({
            "id": str(item.id),
            "institution": item.institution,
            "degree": item.degree,
            "description": item.description,
            "start_year": item.start_year,
            "end_year": item.end_year,
            "star_count": len(starred_users),
            "is_starred": (
                request.user.is_authenticated
                and request.user in starred_users
            ),
        })

    return JsonResponse(data, safe=False)

def show_education(request):
    return render(
        request,
        "education.html",
        {
            "name": "Kevin Ryan Ezekiel",
            "can_add_education": request.user.is_superuser,
            "can_edit_education": can_edit_education(request.user),
            "institution_query": request.GET.get("institution", "").strip(),
        },
    )

def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Kevin Ryan Ezekiel",
        "form": form,
    }
    return render(request, "education_form.html", context)

def update_education(request, education_id):
    if not can_edit_education(request.user):
        raise PermissionDenied
    
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Kevin Ryan Ezekiel",
        "form": form,
    }
    return render(request, "education_form.html", context)

def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Kevin",
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
        "name": "Kevin",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

def can_edit_education(user):
    return (
        user.is_authenticated
        and (user.is_superuser or is_editor(user))
    )

def toggle_education_star(request, education_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Metode request tidak didukung."},
            status=405,
        )

    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Login diperlukan untuk memberi star."},
            status=403,
        )

    education = get_object_or_404(Education, pk=education_id)
    starred_by = education.starred_by

    if starred_by.filter(pk=request.user.pk).exists():
        starred_by.remove(request.user)
        is_starred = False
    else:
        starred_by.add(request.user)
        is_starred = True

    return JsonResponse({
        "star_count": starred_by.count(),
        "is_starred": is_starred,
    })