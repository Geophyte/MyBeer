from django.contrib.auth.models import User

from beers.models import Category, Beer, Comment, Review

def set_up_database(test_class):
    # INIT TEST DATABASE
    test_class.user_1 = User.objects.create_user('user_1', 'user_1@example.com', 'password')
    test_class.user_2 = User.objects.create_user('user_2', 'user_2@example.com', 'password')
    test_class.admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    test_class.category_1 = Category.objects.create(name='Lager')
    test_class.category_1.save()
    test_class.category_2 = Category.objects.create(name='Porter')
    test_class.category_2.save()

    test_class.beer_1 = Beer.objects.create(name='Perła',
                                            description='foobar',
                                            category=test_class.category_1,
                                            created_by=test_class.user_1)
    test_class.beer_2 = Beer.objects.create(name='Warka',
                                            description='barfoo',
                                            category=test_class.category_1,
                                            created_by=test_class.user_2)
    test_class.beer_3 = Beer.objects.create(name='Żywiec porter',
                                            description='foobar',
                                            category=test_class.category_2,
                                            created_by=test_class.user_1)
    test_class.beer_4 = Beer.objects.create(name='inny porter',
                                            description='barfoo',
                                            category=test_class.category_2,
                                            created_by=test_class.user_2)
    test_class.beer_1.save()
    test_class.beer_2.save()
    test_class.beer_3.save()
    test_class.beer_4.save()

    test_class.review_1 = Review.objects.create(title='good',
                                                content='foo bar',
                                                author=test_class.user_1,
                                                beer=test_class.beer_1,
                                                rating=7)

    test_class.review_2 = Review.objects.create(title='not good',
                                                content='foo bar',
                                                author=test_class.user_2,
                                                beer=test_class.beer_1,
                                                rating=2)

    test_class.review_3 = Review.objects.create(title='very good',
                                                content='foo bar',
                                                author=test_class.user_1,
                                                beer=test_class.beer_3,
                                                rating=10)

    test_class.review_4 = Review.objects.create(title='normal',
                                                content='foo bar',
                                                author=test_class.user_2,
                                                beer=test_class.beer_4,
                                                rating=5)
    test_class.review_1.save()
    test_class.review_2.save()
    test_class.review_3.save()
    test_class.review_4.save()

    test_class.comment_1 = Comment.objects.create(author=test_class.user_1,
                                                  review=test_class.review_2,
                                                  content='agree')
    test_class.comment_2 = Comment.objects.create(author=test_class.user_2,
                                                  review=test_class.review_2,
                                                  content='thanks')
    test_class.comment_3 = Comment.objects.create(author=test_class.user_1,
                                                  review=test_class.review_3,
                                                  content='ok')
    test_class.comment_4 = Comment.objects.create(author=test_class.user_1,
                                                  review=test_class.review_4,
                                                  content='kk')

    test_class.comment_1.save()
    test_class.comment_2.save()
    test_class.comment_3.save()
    test_class.comment_4.save()


def activate(model_type):
    for model in model_type.objects.all():
        model.active = True
        model.save()


def deactivate(model_type):
    for model in model_type.objects.all():
        model.active = False
        model.save()
