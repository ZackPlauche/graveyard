from django.db import models

class BlogPost(models.Model):
   title = models.CharField(max_length=255)
   body = models.TextField()
   image = models.ImageField(upload_to='blog_images/')

   def __str__(self):
       return self.title