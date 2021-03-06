from myapp.models import Posts, PostInfo, Followers
from rest_framework import serializers
from django.contrib.auth.models import User as authUser
from rest_framework.response import Response
from rest_framework.views import APIView


class UserSerializer(serializers.Serializer):
    class Meta:
        model = authUser
        fields = ('id', 'username', 'password', 'last_name', 'mail')


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ('id', 'owner', 'date', 'description')


class PostInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostInfo
        fields = ('post_id', 'lx', 'ly', 'map_info', 'img')


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostInfo
        fields = ('post_id', 'owner', 'description', 'date', 'last_modified')


class FollowersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Followers
        fields = ('follower', 'following', 'date')


class TimelineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ('id', 'owner', 'last_modified', 'description')
