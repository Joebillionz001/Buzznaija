from django.db import models

CATEGORY_CHOICES = [
    ('Entertainment', 'Entertainment'),
    ('Sports', 'Sports'),
    ('Politics', 'Politics'),
    ('Business', 'Business'),
    ('Technology', 'Technology'),
    ('World', 'World'),
]

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    short_description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    post_url = models.URLField(max_length=500, unique=True)  # To avoid duplicate posts
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Entertainment')
    published_at = models.DateTimeField()
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at'] # Show newest posts first

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class NewsletterSubscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
