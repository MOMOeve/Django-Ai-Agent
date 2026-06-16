

from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL
# Create your models here.
class Document(models.Model): #Resource
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    title = models.CharField(max_length=100, default="Title", verbose_name="标题")
    content = models.TextField(blank=True, null=True, verbose_name="内容", max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    active = models.BooleanField(default=True, verbose_name="是否活跃")
    active_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name="活跃时段")

    def __str__(self):
        return f"{self.owner} {self.title}"

    def save(self, *args, **kwargs):
        if self.active_at is None and self.active:
            self.active_at = timezone.now()
        else:
            self.active_at = None
        super().save(*args, **kwargs)