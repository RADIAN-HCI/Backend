from rest_framework_nested import routers
from .views import IdeaViewSet


router = routers.SimpleRouter()
router.register(r"ideas", IdeaViewSet, basename="idea")

urlpatterns = router.urls
