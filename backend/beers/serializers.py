from rest_framework import serializers
from beers.models import Beer, Review, Comment, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = ('id', 'name', 'description', 'category', 'created_by', 'image_url', 'rating')

    def create(self, validated_data):
        beer = Beer(name=validated_data['name'],
                    description=validated_data['description'],
                    category=validated_data['category'],
                    created_by=self.context['request'].user)
        beer.save()
        return beer

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['created_by'].read_only = True
        return fields


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
            rating=validated_data['rating'],
            author=self.context['request'].user,
            beer=validated_data['beer']
        )
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
        fields = "__all__"

    def create(self, validated_data):
        comment = Comment(
            author=self.context['request'].user,
            review=validated_data['review'],
            content=validated_data['content']
        )
        comment.save()
        return comment

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['author'].read_only = True
            fields['review'].read_only = True
        return fields
