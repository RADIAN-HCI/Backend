from rest_framework_nested import routers
from .views import AssignmentViewSet
from question.views import QuestionViewSet
from brainstorming.views import BrainstormViewSet

router = routers.SimpleRouter()
router.register(r"assignments", AssignmentViewSet, basename="assignment")

questions_router = routers.NestedSimpleRouter(
    router, r"assignments", lookup="assignment"
)
questions_router.register(
    r"questions", QuestionViewSet, basename="assignment-questions"
)
questions_router.register(
    r"brainstorms", BrainstormViewSet, basename="assignment-brainstorms"
)

urlpatterns = router.urls + questions_router.urls
