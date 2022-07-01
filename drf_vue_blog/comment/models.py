from django.db import models
from django.utils import timezone

from article.models import Article
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    # 实现两级评论，新增parent字段
    parent = models.ForeignKey(
        'self', # 语法限制，不能自己引用自己
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    # 评论人，外键，一对多
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 评论所属文章，外键，一对多
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 评论内容
    content = models.TextField()
    # 评论时间
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.content[:20]
