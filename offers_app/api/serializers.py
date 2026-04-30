from rest_framework import serializers
from django.contrib.auth.models import User
from offers_app.models import OfferModel, OfferDetails
from django.urls import reverse

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

class DetailListSerializer(serializers.ModelSerializer):
    """Serializer für Details in der List-View (nur id und url)"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetails
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

class DetailSerializer(serializers.ModelSerializer):
    """Serializer für Detail-View (vollständige Informationen)"""
    delivery_time_in_days = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = OfferDetails
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type"
        ]
        read_only_fields = ["delivery_time"]

    def validate(self, attrs):
        if "delivery_time_in_days" in attrs:
            attrs["delivery_time"] = attrs.pop("delivery_time_in_days")
        return attrs

class OfferListSerializer(serializers.ModelSerializer):
    """Serializer für List-View mit pagination"""
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = DetailListSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = OfferModel
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_user_details(self, obj):
        user_serializer = UserDetailsSerializer(obj.user, read_only=True)
        return user_serializer.data

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time', flat=True)
        return min(times) if times else None

class OfferSerializer(serializers.ModelSerializer):
    """Serializer für Create/Update"""
    user = serializers.StringRelatedField(read_only=True)
    details = DetailSerializer(many=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = OfferModel
        fields = ["id", "user", "title", "image", "description", "details"]

    def create(self, validated_data):
        user = validated_data.pop("user", None)
        details_data = validated_data.pop("details", [])
        offer = OfferModel.objects.create(user=user, **validated_data)
        for i in details_data:
            OfferDetails.objects.create(offer=offer, **i)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.image = validated_data.get("image", instance.image)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for details_data in details_data:
                OfferDetails.objects.create(offer=instance, **details_data)
        
        return instance