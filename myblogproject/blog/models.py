# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    likes = models.ManyToManyField(
        User, 
        related_name='blog_posts', 
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            try:
                from PIL import Image, ImageOps
                img = Image.open(self.image.path)
                
                # Define target size (e.g., 800x600)
                target_size = (800, 600)
                
                # Always resize/crop to ensure consistency
                img = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS)
                img.save(self.image.path)
            except Exception as e:
                print(f"Error resizing image: {e}")

class Comment(models.Model):
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on'] 

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'