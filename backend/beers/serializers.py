from rest_framework import serializers
from beers.models import Beer, Review, Comment, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = ('id', 'name', 'description', 'category', 'created_by', 'image_url', 'rating', 'active')

    def create(self, validated_data):
        if not self.context['request'].user.is_staff:
            validated_data['active'] = False
        beer = Beer(**validated_data)
        beer.created_by = self.context['request'].user
        beer.save()
        return beer

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['created_by'].read_only = True
            fields['rating'].read_only = True
        return fields


class BeerReadSerializer(BeerSerializer):
    category = CategorySerializer(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'author', 'beer', 'rating', 'active')

    def create(self, validated_data):
        review = Review(**validated_data)
        review.author = self.context['request'].user
        review.active = True
        review.save()
        return review

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['author'].read_only = True
            fields['beer'].read_only = True
        return fields


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'review', 'content', 'active')

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.author = self.context['request'].user
        comment.active = True
        comment.save()
        return comment

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['author'].read_only = True
            fields['review'].read_only = True
        return fields
