from rest_framework import serializers
from django.contrib.auth.models import User
from offers_app.models import OfferModel, OfferDetails

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OfferModel
        fields = ["id", "user", "title", "description"]

class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetails
        fields = ["id", "title", "revisions", "delivery_time", "price", "features"]