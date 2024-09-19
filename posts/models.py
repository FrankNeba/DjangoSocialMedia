from django.db import models
from authenticate.models import User

# Create your models here.
class Image(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=200)
    image = models.ImageField(upload_to='media/images/posts', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(null=True)
    like = models.PositiveIntegerField(default = 0)
    images = models.ManyToManyField(Image)
    video = models.FileField(upload_to='media/videos', null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        name = f'{self.user.username}: {self.text[:20]}'
        return name
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} : {self.post.text[:20]}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} : {self.text[:20]}'
