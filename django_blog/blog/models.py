from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length= 200)
    content = models.TextField()
    published_date = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title