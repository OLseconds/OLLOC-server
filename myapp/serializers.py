from myapp.models import User, Posts
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
        fields = ('post_id', 'owner', 'last_modified', 'description', 'contents')


