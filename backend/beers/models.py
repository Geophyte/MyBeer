import statistics

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Beer(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    active = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=150, null=False)
    content = models.TextField()
    rating = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(10)])
    active = models.BooleanField(null=False)

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        beer_reviews = Review.objects.filter(beer=self.beer.pk, active=True)
        beer = Beer.objects.get(pk=self.beer.pk)
        if beer_reviews:
            new_rating = statistics.mean([review.rating for review in beer_reviews])
            beer.rating = new_rating
        else:
            beer.rating = self.rating
        beer.save()

    def delete(self, *args, **kwargs):
        beer = Beer.objects.get(pk=self.beer.pk)
        beer_reviews = Review.objects.filter(beer=self.beer.pk).exclude(pk=self.pk)
        super(Review, self).delete(*args, **kwargs)
        if beer_reviews:
            new_rating = statistics.mean([review.rating for review in beer_reviews if review.active])
            beer.rating = new_rating

        else:
            beer.rating = None
        beer.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    active = models.BooleanField(null=False, default=False)

    def __str__(self):
        return str(self.author) + " comment"
