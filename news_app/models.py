from django.urls import reverse
from django.utils import timezone
from django.db import models



# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)

class Category(models.Model):
    objects = None
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class News(models.Model):

    class Status(models.TextChoices):
        Draft = "DR", "Draft"
        Published = "PB", "Published"
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to="news_app/images/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, default="draft", choices=Status.choices)
    objects = models.Manager() #default
    published = PublishedManager()

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_app:detail", kwargs={"slug": self.slug})


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email
