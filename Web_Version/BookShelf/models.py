import uuid

from django.db import models

# Create your models here.

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('В наличии', 'В наличии'),
        ('Выдана', 'Выдана')
    ], default='В наличии')
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True, default='book_covers/default_cover.png')
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
