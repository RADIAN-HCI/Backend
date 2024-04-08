from rest_framework_nested import routers
from .views import CourseViewSet
from assignment.views import AssignmentViewSet

router = routers.SimpleRouter()
router.register(r"courses", CourseViewSet, basename="assignment")

assignments_router = routers.NestedSimpleRouter(router, r"courses", lookup="course")
assignments_router.register(
    r"assignments", AssignmentViewSet, basename="course-assignments"
)

urlpatterns = router.urls + assignments_router.urls
