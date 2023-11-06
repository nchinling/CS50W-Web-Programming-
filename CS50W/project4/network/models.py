from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content=models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user} | Post Id: {self.id} | Date: {self.date.strftime('%d %b %Y %H:%M:%S')} "

class Follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_that_is_following")
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_being_followed")

    def __str__(self):
        return f"{self.user} follows {self.follows}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post")

    def __str__(self):
        return f"{self.post} liked by {self.user}"
