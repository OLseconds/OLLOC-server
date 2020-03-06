from myapp.models import User, Posts, PostInfo
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'mail')


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ('id', 'owner', 'last_modified', 'description')


class PostInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostInfo
        fields = ('post_id', 'lx', 'ly', 'img')


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostInfo
        fields = ('post_id', 'owner', 'description', 'date', 'last_modified')