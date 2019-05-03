from django.db import models
from django.utils import timezone

class Post(models.Model):  #Django knows that it should be saved in DB.
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Image(models.Model):
    photo = models.ImageField(upload_to='images/', verbose_name='添付画像')
    description = models.CharField(max_length=255, blank=True, verbose_name='説明')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.photo.url  #一応URLがでる。
