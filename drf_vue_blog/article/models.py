from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown

# Create your models here.

# 分类
class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

# 标签
class Tag(models.Model):
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.text

# 文章标题图
class Avatar(models.Model):
    content = models.ImageField(upload_to=r'avatar/%Y%m%d')

#博客文章 model
class Article(models.Model):
    # 分类，外键
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    # 标签，多对多
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    # 作者，外键
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='articles')
    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)
    # 标题图，外键，但是一对一，所以related_name为article而不是articles
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title

    # 将body转换为带html标签的正文
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc是渲染后的目录
        return md_body, md.toc

