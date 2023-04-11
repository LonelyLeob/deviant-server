from rest_framework import serializers
from .models import Girl, Link, Avatar

class LinkSerializer(serializers.ModelSerializer):
    pic = serializers.ImageField()
    class Meta:
        model = Link
        fields = ['title', 'link', 'pic']

class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = Avatar
        fields = ['avatar']

class GirlSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True)
    avatars = AvatarSerializer(many=True)

    class Meta:
        model = Girl
        fields = ['avatars', 'nickname', 'additional_info',  'links']