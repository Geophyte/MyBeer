import statistics
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def upload_to(instance, filename):
    f_name, f_type = filename.split('.')
    f_hash = hash(f_name)
    return 'images/{filename}'.format(filename=f"{f_hash}.{f_type}")


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Beer(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=None, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    image_url = models.ImageField(upload_to=upload_to, null=True, default='images/default.png')
    active = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=0, editable=False)

    def delete(self, *args, **kwargs):
        reviews = Review.objects.filter(beer=self.pk)
        reviews.delete()
        super(Beer, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=150, null=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    rating = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        reviews = Review.objects.filter(beer=self.beer.pk, active=True, beer__active=True)
        beer = Beer.objects.get(pk=self.beer.pk)
        if reviews:
            beer.rating = statistics.mean([review.rating for review in reviews])
        else:
            beer.rating = 0
        beer.save()

    def delete(self, *args, **kwargs):
        comments = Comment.objects.filter(review=self.pk)
        comments.delete()

        beer = Beer.objects.get(pk=self.beer.pk)
        super(Review, self).delete(*args, **kwargs)
        reviews = Review.objects.filter(beer=beer.pk, active=True, beer__active=True).exclude(pk=self.pk)

        if reviews:
            beer.rating = statistics.mean([review.rating for review in reviews])
        else:
            beer.rating = 0
        beer.save()

    def __str__(self):
        return f"title: {self.title}, beer: {self.beer.name}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"author: {str(self.author)}, review: {self.review.title}, beer: {self.review.beer.name}"
