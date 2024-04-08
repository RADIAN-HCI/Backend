from rest_framework_nested import routers
from .views import BrainstormViewSet
from idea.views import IdeaViewSet

router = routers.SimpleRouter()
router.register(r"brainstorms", BrainstormViewSet, basename="brainstorm")

ideas_router = routers.NestedSimpleRouter(router, r"brainstorms", lookup="brainstorm")
ideas_router.register(r"ideas", IdeaViewSet, basename="brainstorm-ideas")

urlpatterns = router.urls + ideas_router.urls
