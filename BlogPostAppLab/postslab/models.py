from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=100,null=False,blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    files=models.FileField(upload_to='files/')
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    date_left = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)

class PostUser(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   first_name = models.CharField(max_length=50)
   last_name = models.CharField(max_length=50)

   def __str__(self):
       return self.first_name + " " + self.last_name


class BlockedUser(models.Model):
    blockedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    postUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')