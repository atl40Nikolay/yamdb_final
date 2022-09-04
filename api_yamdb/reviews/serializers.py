from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Comment, Review, Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        request = self.context.get('request')
        title_id = request.parser_context.get('kwargs').get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        # request = self.context['request']
        # title_id = self.context.get('view').kwargs.get('title_id')
        # title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=title, author=request.user
            ).exists()
        ):
            raise serializers.ValidationError('Only one review.')
        return data

    class Meta:
        model = Review
        fields = ('id', 'title', 'author', 'text', 'pub_date', 'score')
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['author', 'title']
        #     )
        # ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'author', 'text', 'pub_date')
