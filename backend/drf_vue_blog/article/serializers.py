from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from article.models import Article, Category, Tag, Avatar
from comment.serializers import CommentSerializer
from user_info.serializers import UserDescSerializer

# 这样子的写法过于繁琐，而且还要写得和对应的model字段一一对应，不好，推荐用模型序列化器ModelSerializer
# class ArticleListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(allow_blank=True, max_length=100)
#     body = serializers.CharField(allow_blank=True)
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()

# 文章列表的序列化器，只需要这三个属性
class ArticleListSerializer(serializers.ModelSerializer):
    author = UserDescSerializer(read_only=True) # 这个要放到Meta的外面
    # HyperlinkedIdentityField是DRF框架提供的超链接字段，只需要你在参数里提供路由的名称，它就自动帮你完成动态地址的映射。
    # view_name是路由的名称，也就是我们在path(... name='xxx')里的那个name
    url = serializers.HyperlinkedIdentityField(view_name="article:detail")
    class Meta:
        # 自动推断需要序列化的字段及类型
        # 提供对字段数据的验证器的默认实现
        # 提供了修改数据需要用到的 .create() 、 .update() 方法的默认实现
        model = Article
        fields = [
            'author',
            'title',
            'created',
            'url',
        ]

# 给分类详情的嵌套序列化器
class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='article-detail') # 分类详情页面要显示该分类下的所有文章

    class Meta:
        model = Article
        fields = [
            'url',
            'title'
        ]

# 分类详情
class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]

# 分类视图集的序列化器
class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail') # ？

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']

# 标签视图集序列化器
class TagSerializer(serializers.ModelSerializer):
    '''同text不同id的标签是不被允许的，因此在创建或者更新标签的时候要进行存在性检查，如果标签已存在，就报个错'''
    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)
    class Meta:
        model = Tag
        fields = '__all__'

# 标题图视图集序列化器
class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'

# 由于文章详情和文章列表需要的字段大部分相同，因此抽象出父类
# 这个HyperlinkedModelSerializer在ModelSerializer的基础上多了个自动关联的超链接外键字段，并且默认不包含模型对象的id字段
class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    # 文章作者的嵌套序列化字段
    author = UserDescSerializer(read_only=True)
    # 文章分类的嵌套序列化字段
    category = CategorySerializer(read_only=True)
    # 分类的id，用于创建/更新文章分类
    # DRF框架原生没有实现可写的嵌套数据（因为其操作逻辑没有统一的标准），那我想创建/更新文章和分类的外键关系怎么办？
    # 一种方法是自己去实现序列化器的create()/update()方法；另一种就是DRF框架提供的修改外键的快捷方式，
    # 即显式指定category_id字段，则此字段会自动链接到category外键，以便你更新外键关系。
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    # 标签字段，使用SlugRelatedField来直接显示text字段的内容
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )
    # 文章标题图字段，要对id进行有效性检查
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)


    # 两个验证器逻辑相似，可以整合一下：
    # 自定义错误信息
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..'
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(
            model=Avatar,
            value=value,
            message='incorrect_avatar_id'
        )

        return value

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(
            model=Category,
            value=value,
            message='incorrect_category_id'
        )

        return value
    # category_id字段验证器，以防用户提交一个不存在的分类id
    # 验证方式又有如下几种：
    # 覆写序列化器的.validate(...)方法。这是个全局的验证器，其接收的唯一参数是所有字段值的字典。当你需要同时对多个字段进行验证时，这是个很好的选择。
    # 另一种就是本项目用到的，即.validate_{field_name}(...)方法，它会只验证某个特定的字段，比如category_id。
    # def validate_category_id(self, value):
    #     if not Category.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError("Category with id {} not exists.".format(value))
    #     return value

    # def validate_avatar_id(self, value):
    #     if not Avatar.objects.filter(id=value).exists() and value is not None:
    #         raise serializers.ValidationError("Avatar with id {} not exists".format(value))
    #     return value

    def to_internal_value(self, data):
        '''当要给文章贴的标签不存在时，自动创建'''
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
        return super().to_internal_value(data)

# 提供给文章视图集的序列化器
class ArticleSerializer(ArticleBaseSerializer):
    # 内部类不会隐式从父类继承，因此最好显示声明
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body' : {'write_only' : True}} # 列表接口不需要显示body，因此用这句话将body变为仅可写却不显示

# 文章详情的序列化器，需要全部属性
class ArticleDetailSerializer(ArticleBaseSerializer):
    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    # 被body_html字段自动调用，并将返回结果作为需要序列化的数据，其中的obj是序列化器获取到的model实例，也就是文章对象
    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1] 

    class Meta:
        model = Article
        fields = '__all__'

# 给非管理员用户查看文章详情时使用的序列化器，不返回body
class ArticleDetailExceptBodySerializer(ArticleDetailSerializer):
    class Meta:
        model = Article
        exclude=['body'] # 非管理员查询文章详情时，隐藏body



