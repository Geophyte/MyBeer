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
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    image_url = models.ImageField(upload_to=upload_to, default='images/default.png')
    # active = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, editable=False)

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=150, null=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    # active = models.BooleanField(null=False, default=False)
    rating = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        reviews = Review.objects.filter(beer=self.beer.pk)
        beer = Beer.objects.get(pk=self.beer.pk)
        if reviews:
            beer.rating = statistics.mean([review.rating for review in reviews])
        else:
            beer.rating = self.rating
        beer.save()

    def delete(self, *args, **kwargs):
        beer = Beer.objects.get(pk=self.beer.pk)
        super(Review, self).delete(*args, **kwargs)
        reviews = Review.objects.filter(beer=beer.pk).exclude(pk=self.pk)

        if reviews:
            beer.rating = statistics.mean([review.rating for review in reviews])
        else:
            beer.rating = None
        beer.save()

    # def delete(self, *args, **kwargs):
    #     beer = Beer.objects.get(pk=self.beer.pk)
    #     beer_reviews = Review.objects.filter(beer=self.beer.pk).exclude(pk=self.pk)
    #     super(Review, self).delete(*args, **kwargs)
    #     if beer_reviews:
    #         new_rating = statistics.mean([review.rating for review in beer_reviews])
    #         beer.rating = new_rating
    #
    #     else:
    #         beer.rating = None
    #     beer.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, editable=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()

    # active = models.BooleanField(null=False, default=False)

    def __str__(self):
        return str(self.author) + " comment"
