from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from question.views import QuestionViewSet
from assignment.views import AssignmentViewSet
from assignment.views import generate_pdf_api
from course.views import CourseViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"assignments", AssignmentViewSet, basename="assignment")
# router.register(r"users", UserViewSet, basename="user")
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path(
        "api/",
        include(
            [
                path("", include(router.urls)),
                path("auth/", include("djoser.urls")),
                path("auth/", include("djoser.urls.jwt")),
            ]
        ),
    ),
    path("generate_pdf/", generate_pdf_api, name="generate_pdf_api"),
    path("admin/", admin.site.urls),
]
