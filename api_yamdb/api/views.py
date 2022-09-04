import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS
from reviews.models import Category, Genre, Title
from users.permissions import IsMyAdminOrReadOnly

from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesGetSerializer, TitlesPostSerializer)


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name="genre__slug",
        lookup_expr='exact'
    )
    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr='exact'
    )
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr='contains'
    )
    description = django_filters.CharFilter(
        field_name="description",
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsMyAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsMyAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsMyAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return TitlesPostSerializer
        return TitlesGetSerializer
