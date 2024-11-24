from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from account.models import CustomUser
User = CustomUser


# Create your models here.

class Author(models.Model):
    author_dp = models.ImageField(upload_to='author dp')
    author_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True)


    def __str__(self):
        return self.author_name
    

class BlogCategory(models.Model):
    title = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True)


    def __str__(self):
        return self.title
    


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Blog(models.Model):
    blog_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=250)
    blog_cover = models.ImageField(upload_to='Blog image/')
    blog_content = models.TextField()
    blog_image_one = models.ImageField(upload_to='Blog image/')
    blog_image_two = models.ImageField(upload_to='Blog image/')
    quotes = models.TextField()
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blog_title} -- {self.blog_author}"


class BlogInteraction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'blog')  # Ensure each user can only interact with each blog once


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make user optional
    user_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=75)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name

    

class SubComment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='subcomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=75)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
    

class Newsletter(models.Model):
    pass


def create_slug(instance, new_slug=None):
    if isinstance(instance, Blog):
        slug = slugify(instance.blog_title)
    elif isinstance(instance, BlogCategory):
        slug = slugify(instance.title)
    elif isinstance(instance, Author):
        slug = slugify(instance.author_name)
    else:
        return None

    if new_slug is not None:
        slug = new_slug
    
    ModelClass = instance.__class__
    qs = ModelClass.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=Blog)
@receiver(pre_save, sender=BlogCategory)
@receiver(pre_save, sender=Author)
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)