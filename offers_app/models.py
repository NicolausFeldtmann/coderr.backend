from django.db import models
from django.contrib.auth.models import User

class OfferModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=160)

class OfferDetails(models.Model):
    offer = models.ForeignKey(OfferModel, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=30)
    revisions = models.IntegerField(blank=True, null=True, default="")
    delivery_time = models.IntegerField()
    price = models.IntegerField()
    features = models.CharField(max_length=20)

