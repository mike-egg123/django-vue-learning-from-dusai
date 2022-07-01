from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from article.models import Article, Category, Tag, Avatar
from article.serializers import ArticleListSerializer, ArticleDetailSerializer,ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, ArticleDetailExceptBodySerializer, AvatarSerializer
from article.permissions import isAdminUserOrReadOnly
from article.filters import ArticleTitleFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets,filters
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.template.context_processors import csrf
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
import json

# Create your views here.

'''
# 这是较为原始的返回Json的方式
def article_list(request):
    articles = Article.objects.all()
    serializer = ArticleListSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe=False)
'''


# 视图函数的写法，抛弃，全面转成视图类
# drf提供了对视图函数的扩展，可以限制该视图接收的请求类型，提供了封装好的状态号以及Response，它可以根据内容协商来确定返回给客户端的正确内容类型
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 文章列表，查文章列表信息以及新增文章（只能新增标题，内容还需后序调用文章详情的接口修改内容）
class ArticleList(generics.ListCreateAPIView):
    permission_classes = [isAdminUserOrReadOnly] # 请求必须满足列表中的所有权限条件才可以放行
    queryset = Article.objects.all() # 视图类要用到的数据
    serializer_class = ArticleListSerializer # 将数据序列化并传送给前端的序列化器
    # 新增的这个perform_create()从父类ListCreateAPIView继承而来，它在序列化数据真正保存之前调用，因此可以在这里添加额外的数据（即用户对象）。
    # serializer参数是ArticleListSerializer序列化器实例，并且已经携带着验证后的数据。它的save()方法可以接收关键字参数作为额外的需要保存的数据。
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

'''
# 以下这种写法还略显麻烦，还需自己处理业务逻辑
# 文章详情类视图，带有DRF扩展
class ArticleDetail(APIView):
    """文章详情视图"""

    def get_object(self, pk):
        """获取单个文章对象"""
        try:
            # pk 即主键，默认状态下就是 id
            return Article.objects.get(pk=pk)
        except:
            raise Http404

    # 获取文章详情
    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        # 返回 Json 数据
        return Response(serializer.data)

    # 更改文章内容
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data)
        # 验证提交的数据是否合法
        # 不合法则返回400
        if serializer.is_valid():
            # 序列化器将持有的数据反序列化后，
            # 保存到数据库中
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 删除文章
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        # 删除成功后返回204
        return Response(status=status.HTTP_204_NO_CONTENT)

# 使用mixin类，使删改查更简单
class ArticleDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
'''
# 还可以更简单：
# 文章详情，删、改、查文章
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdminUserOrReadOnly]
    queryset = Article.objects.all() # 与文章列表视图类获取的数据是一样的，但序列化器不一样，导致接口得到的数据也有所区别
    serializer_class = ArticleDetailSerializer

# 更更简单，文章视图集！高度集成，包含了列表查，详情查，增删改
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [isAdminUserOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            # 对于管理员，返回body，否则不返回body
            if self.request.user.is_superuser:
                return ArticleDetailSerializer
            else:
                return ArticleDetailExceptBodySerializer

# 分类视图集
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [isAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer

# 标签视图集
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [isAdminUserOrReadOnly]
    serializer_class = TagSerializer

# 上传图片的流程如下：
# 1.发表新文章时，标题图需要先上传。
# 2.标题图上传完成会返回其数据（比如图片数据的 id）到前端并暂存，等待新文章完成后一起提交。
# 3.提交新文章时，序列化器对标题图进行检查，如果无效则返回错误信息。
# 标题图视图集
class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    permission_classes = [isAdminUserOrReadOnly]
    serializer_class = AvatarSerializer # DRF已经封装好了对图片的处理，不需要关心细节，只需要像其他JSON接口一样写序列化器即可

# drf强制跨域了，通过这个接口来获取crsf_token，然后发post请求的时候参数里带上"csrfmiddlewaretoken":csrf_token
def get_csrf(request):
        #生成 csrf 数据，发送给前端
    x = csrf(request)
    csrf_token = x['csrf_token']
    return HttpResponse('{}'.format(csrf_token))
