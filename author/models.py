from django.db import models



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    author_picture = models.ImageField(default="default_cover.jpg")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

