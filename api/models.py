from django.db import models

# Create your models here.
class Quote(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    author = models.CharField(max_length = 255)
    content = models.TextField()
    tags = models.JSONField(default=list)

    def __str__(self):
        return f'{self.content} -- {self.author}'
