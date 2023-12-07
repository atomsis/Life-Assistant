from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
###--------Отдельный контекстный менеджер----------------------------------------------
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TodoList.Status.PUBLISHED)
###-----------------------------------------------------------------------------------

class TodoList(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF','DRAFT'
        PUBLISHED = 'PB','PUBLISHED'


    tags = TaggableManager()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    tasks = models.TextField()
    description = models.TextField(max_length=255)
    #slug = models.CharField(max_length=255,unique=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date'])
        ]

    def __str__(self):
        return f"{self.user}'s TodoList for {self.date}"

    def get_absolute_url(self):
        return reverse('todo:task_detail',
                       # args=[self.date.strftime('%Y-%m-%d')])
                        args=[self.date.year, self.date.month, self.date.day])

class Comment(models.Model):
    task = models.ForeignKey(TodoList,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Комментарий к списку задач {self.task},от {self.name}'