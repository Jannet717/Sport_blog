from django.db import models

from account.models import User


class Category(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return str(self.comment)

    class Meta:
        ordering = ('-created',)


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')



    def __str__(self):
        return str(self.likes)


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.rating)

class Favorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)
    #
    # def __str__(self):
    #     return str(self.favorite)




