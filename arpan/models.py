from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from account.models import CustomUser
User = CustomUser


class ProjectCategory(models.Model):
    PROGRAMMING_LANGUAGE = (
        ('Python', 'Python'),
        ('Django', 'Django'),
        ('Vanila Javascript', 'Vanila Javascript'),
        ('Node Js', 'Node Js'),
        ('WordPress', 'WordPress'),
        ('Laravel', 'Laravel'),
    )
    programming_laguage = models.CharField(
        choices=PROGRAMMING_LANGUAGE, max_length=200)
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True)

    def __str__(self):
        return self.programming_laguage
    


class Project(models.Model):
    PROJECT_FOR = (
        ('Clients', 'Clients'),
        ('Personal', 'Personal'),

    )
    PROJECT_STATUS = (
        ('Complete', 'Complete'),
        ('Working', 'Working'),

    )
    project_category = models.ForeignKey(
        ProjectCategory, on_delete=models.CASCADE, related_name='project_category')
    project_name = models.CharField(max_length=250)
    project_type = models.CharField(choices=PROJECT_FOR, max_length=200)
    project_staus = models.CharField(choices=PROJECT_STATUS, max_length=200)
    main_image = models.ImageField(upload_to='Project Image')
    project_heading = models.CharField(max_length=50)
    project_short_dec = models.CharField(max_length=255)
    project_keypoint1 = models.CharField(max_length=50)
    project_keypoint2 = models.CharField(max_length=50)
    project_keypoint3 = models.CharField(max_length=50)
    project_keypoint4 = models.CharField(max_length=50)
    related_image1 = models.ImageField(upload_to='Project Image')
    related_image2 = models.ImageField(upload_to='Project Image')
    related_image3 = models.ImageField(upload_to='Project Image')
    scrollable_image = models.ImageField(upload_to='Project Image')
    text_for_scrollable_img = models.CharField(max_length=255)
    conclusion_img = models.ImageField(upload_to='Project Image')
    conclusion_txt = models.CharField(max_length=255)
    conclusion_keypoint1 = models.CharField(max_length=50)
    conclusion_keypoint2 = models.CharField(max_length=50)
    conclusion_keypoint3 = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True)

    def __str__(self):
        return self.project_name
    

def create_slug(instance, new_slug=None):
    if isinstance(instance, ProjectCategory):
        slug = slugify(instance. programming_laguage)
    elif isinstance(instance, Project):
        slug = slugify(instance.project_name)
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


@receiver(pre_save, sender=ProjectCategory)
@receiver(pre_save, sender=Project)
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
