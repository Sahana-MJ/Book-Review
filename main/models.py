from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Book(models.Model):
    name= models.CharField(max_length=300)
    author=models.CharField(max_length=300)
    description = models.TextField(max_length=5000,default=None,null=True)
    published_year=models.DateField()
    averagerating=models.FloatField(default=0)
    image = models.URLField(default=None,null=True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
