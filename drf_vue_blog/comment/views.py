from django.shortcuts import render
from comment.models import Comment
from comment.permissions import IsOwnerOrReadOnly
from comment.serializers import CommentSerializer
from rest_framework import viewsets


# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
