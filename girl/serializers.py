from rest_framework import serializers
from django.contrib.gis.geoip2 import GeoIP2
from .models import Girl, Link, Avatar

class LinkSerializer(serializers.ModelSerializer):
    pic = serializers.ImageField()
    class Meta:
        model = Link
        fields = ['title', 'link', 'pic', 'flag']

class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = Avatar
        fields = ['avatar']

class GirlSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True)
    avatars = AvatarSerializer(many=True)
    geo = serializers.SerializerMethodField("_geo")

    class Meta:
        model = Girl
        fields = ['avatars', 'nickname', 'additional_info',  'links', 'geo']

    def _geo(self, _: Girl):
        x_forwarded_for = self.context['request'].META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.context['request'].META.get('REMOTE_ADDR')
        geocoder = GeoIP2()
        # if ip == "127.0.0.1":
        #     return "Moscow"
        return geocoder.city(ip)['city']