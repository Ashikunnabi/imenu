from rest_framework import serializers

from apps.home.models import (
    Carousel,
    PromoSection,
    Page,
    Banner,
    Flyer,
    NavCategory,
    Notice,
    Event,
    UsefulLinks
)

from apps.inventory.models import Brand


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'


class PromoSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoSection
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    human_readable_page = serializers.StringRelatedField(source='page')

    class Meta:
        model = Banner
        fields = '__all__'


class BrandImageOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'image', 'hashed_id']


class FlyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flyer
        fields = '__all__'


class NavCategorySerializer(serializers.ModelSerializer):
    human_readable_parent = serializers.StringRelatedField(source='parent')

    class Meta:
        model = NavCategory
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class UsefulLinksSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsefulLinks
        fields = '__all__'


class DashboardSummarySerializer(serializers.Serializer):
    code = serializers.CharField()
    title = serializers.CharField()
    count = serializers.IntegerField()
