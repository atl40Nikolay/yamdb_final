from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CommentsViewSet, ReviewsViewSet

app_name = 'reviews'

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
