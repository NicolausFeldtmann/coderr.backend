from rest_framework import serializers
from django.contrib.auth.models import User
from offers_app.models import OfferModel, OfferDetails

class DetailSerializer(serializers.ModelSerializer):
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

class OfferSerializer(serializers.ModelSerializer):
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