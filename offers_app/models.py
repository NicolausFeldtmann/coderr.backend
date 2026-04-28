from django.db import models
from django.contrib.auth.models import User

class OfferModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="offers/", null=True, blank=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.title

class OfferDetails(models.Model):
    offer = models.ForeignKey(OfferModel, related_name="details", null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    revisions = models.IntegerField(blank=True, null=True, default=0)
    delivery_time = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return f"{self.offer.title} - {self.title}"