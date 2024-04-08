from rest_framework_nested import routers
from .views import QuestionViewSet


router = routers.SimpleRouter()
router.register(r"questions", QuestionViewSet, basename="question")

urlpatterns = router.urls
