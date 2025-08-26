from django.db import models

# Create your models here.
class Quote(models.Model):
    """
    A database model which stores quotes by their content, author and tags.
    """
    pkid = models.BigAutoField(primary_key=True)
    author = models.CharField(max_length = 255)
    content = models.TextField()
    tags = models.JSONField(default=list)
    embedding = models.JSONField(default=list)

    def __str__(self):
        return f'{self.content} -- {self.author}'
