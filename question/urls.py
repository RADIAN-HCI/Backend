from rest_framework_nested import routers
from .views import QuestionViewSet, image_detail, QuestionListByAssignment
from django.urls import path


router = routers.SimpleRouter()
router.register(r"questions", QuestionViewSet, basename="question")

# router.register(r'images', ImageViewSet, basename='image')

urlpatterns = router.urls + [
    path('images/<str:filename>/', image_detail, name='image_detail'),
    path('questions/sorted/<int:assignment_id>/', QuestionViewSet.as_view({'get': 'list_sorted_for_assignment'}), name='question-list-sorted'),
    path('questions/order/<int:assignment>/', QuestionViewSet.as_view({'put': 'update_order_for_assignment'}), name='question-update-order'),
    path('questions/assignment/<int:assignment_id>/', QuestionListByAssignment.as_view(), name='questions-by-assignment'),
]

# urlpatterns = router.urls
