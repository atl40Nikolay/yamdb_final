from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import IsStaffOrAuthorOrReadOnly

from .models import Review, Title
from .serializers import CommentsSerializer, ReviewsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer

    # def get_serializer_context(self):
    #     serializer = ReviewsSerializer.include_extra_kwargs
    #     context = super(CommentsViewSet, self).get_serializer_context()
    #     return context

    def perform_create(self, serializer):
        ReviewsSerializer.get_initial
        # print(f'KWARGS_VIEW: {self.kwargs}\n')
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        # extra_kwargs = {'title': title, }

        # print(f'KWARGS_SERIALIZER: {serializer.get_extra_kwargs()}\n')
        # serializer.include_extra_kwargs(extra_kwargs)
        # print(f'KWARGS_SERIALIZER_MODIFIED:
        # {serializer.get_extra_kwargs(extra_kwargs)}\n')
        # print(f'INSTANCE: {serializer.instance}\n')
        # print(f'CONTEXT: {serializer.context}\n')
        # print(f'DIR: {serializer.__dir__()}')
        serializer.save(title=title, author=self.request.user)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsStaffOrAuthorOrReadOnly]
        return [permission() for permission in permission_classes]


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsStaffOrAuthorOrReadOnly]
        return [permission() for permission in permission_classes]
