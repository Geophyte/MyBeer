from rest_framework import serializers

from beers.models import Beer, Review, Comment, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = ('id', 'name', 'description', 'category', 'created_by', 'image_url', 'active', 'rating')


class BeerReadSerializer(BeerSerializer):
    category = CategorySerializer(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        review = Review(
            title=validated_data['title'],
            content=validated_data['content'],
            active=True,
            rating=validated_data['rating'],
            author=self.context['request'].user
        )
        review.save()
        return review


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        comment = Comment(
            author=self.context['request'].user,
            review=validated_data['review'],
            content=validated_data['content'],
            active=True
        )
        comment.save()
        return comment
