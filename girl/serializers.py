from rest_framework import serializers
from .models import Girl, Link

class LinkSerializer(serializers.ModelSerializer):
    pic = serializers.ImageField()
    class Meta:
        model = Link
        fields = ['title', 'link', 'pic']

class GirlSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    links = LinkSerializer(many=True)

    class Meta:
        model = Girl
        fields = ['avatar', 'nickname', 'additional_info',  'links']