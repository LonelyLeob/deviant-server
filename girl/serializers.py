from rest_framework import serializers
from .models import Girl, Link, Avatar
from .utils import func_table

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['title', 'link', 'flag']

class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = Avatar
        fields = ['avatar']

class GirlSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True)
    avatars = AvatarSerializer(many=True)
    additional_info = serializers.SerializerMethodField("_info")

    class Meta:
        model = Girl
        fields = ['avatars', 'nickname', 'additional_info',  'links']

    def _info(self, obj: Girl):
        tag = obj.additional_info[obj.additional_info.find("{")+len("{"):obj.additional_info.rfind("}")]
        if tag in func_table:
            return obj.additional_info.replace("{"+tag+"}", func_table[tag](self.context["request"]))
        return obj.additional_info