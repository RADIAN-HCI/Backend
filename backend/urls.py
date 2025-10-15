from django.contrib import admin
from django.urls import path, include
from assignment.views import generate_pdf_api, assignment_pdf_view

urlpatterns = [
    path("api/", include("question.urls")),
    path("api/", include("course.urls")),
    path("api/", include("assignment.urls")),
    path("api/", include("brainstorming.urls")),
    path("api/", include("idea.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("generate_pdf/", generate_pdf_api, name="generate_pdf_api"),
    path("assignment_pdf.pdf", assignment_pdf_view, name="assignment_pdf"),
    path("admin/", admin.site.urls),
]
