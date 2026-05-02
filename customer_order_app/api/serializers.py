from rest_framework import serializers
from customer_order_app.models import OrderModel
from offers_app.models import OfferDetails
from django.contrib.auth.models import User

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "offer_detail",
            "customer_user",
            "buisness_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "customer_user", "buisness_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "created_at", "updated_at"]

class CreateOrderSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        offer_detail_id = validated_data.get("offer_detail_id")
        user = self.context["request"].user

        try:
            offer_detail = OfferDetails.objects.get(id=offer_detail_id)
        except OfferDetails.DoesNotExist:
            raise serializers.ValidationError({"error": "Offer detail not found."})

        order = OrderModel.objects.create(
            offer_detail=offer_detail,
            customer_user=user,
            buisness_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='pending'
        )
        return order
        return order