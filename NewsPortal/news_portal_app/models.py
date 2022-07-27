from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    userA = models.OneToOneField(User, on_delete = models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('post_rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.userA.comment_set.aggregate(commentRating=Sum('comments_rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    theme = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    NEWS = "NW"
    ARTICLE = "AR"
    CATEGORIES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    article_or_news = models.CharField(max_length=2, choices=CATEGORIES, default=NEWS)
    heading = models.CharField(max_length=255)
    text_article = models.TextField()
    post_rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return '{}\n{}...'.format(self.heading, self.text_article[0:123])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text_of_comment = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comments_rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comments_rating += 1
        self.save()

    def dislike(self):
        self.comments_rating -= 1
        self.save()