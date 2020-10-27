from .models import News

from rest_framework import serializers


class NewsListSerializer(serializers.ModelSerializer):
    creators = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = News
        fields = ('id', 'created_date', 'image', 'title', 'short_description', 'creators')

    # def create(self, validated_data):
    #     news = News.objects.create(**validated_data)
    #     news.creators = self.context['request_user']
    #     news.save()
    #     return news


class NewsDetailSerializer(serializers.ModelSerializer):
    creators = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = News
        fields = ('id', 'created_date', 'updated_date', 'image', 'title', 'description', 'short_description',
                  'creators')
    #
    # def create(self, validated_data):
    #     news = News.objects.create(**validated_data)
    #     news.creators = self.context['request_user']
    #     news.save()
    #     return news