from django.contrib import admin
from django.urls import path, include
from assignment.views import generate_pdf_api

urlpatterns = [
    path("api/", include("question.urls")),
    path("api/", include("course.urls")),
    path("api/", include("assignment.urls")),
    path("api/", include("brainstorming.urls")),
    path("api/", include("idea.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("generate_pdf/", generate_pdf_api, name="generate_pdf_api"),
    path("admin/", admin.site.urls),
]
