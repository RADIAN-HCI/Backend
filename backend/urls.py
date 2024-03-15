from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from question.views import QuestionViewSet
from assignment.views import AssignmentViewSet
from assignment.views import generate_pdf_api
from user.views import UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('generate_pdf/', generate_pdf_api, name='generate_pdf_api'),
    path('admin/', admin.site.urls),
]
