from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles', TitlesViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
