from rest_framework import serializers

from comment.models import Comment
from user_info.serializers import UserDescSerializer

class CommentChildrenSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['parent', 'article']

class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)
    # 评论所属文章的超链接
    # HyperlinkedIdentityField用于对自身模型进行超链接，而HyperlinkedRelatedField用于对外键模型进行超链接
    article = serializers.HyperlinkedRelatedField(view_name='article-detail', read_only=True)
    article_id = serializers.IntegerField(write_only=True, allow_null=False, required=True)
    # 评论所属父评论
    parent = CommentChildrenSerializer(read_only=True)
    parent_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    def update(self, instance, validated_data):
        # 父评论只有创建时才可以关联，后续不能更改，即一开始评论了一个评论，后面不可以将这个评论转移到另一个评论下，因此在这里忽略掉parent_id
        validated_data.pop('parent_id', None)
        validated_data.pop('article_id', None)
        return super().update(instance, validated_data)
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'created':{'read_only':True}}