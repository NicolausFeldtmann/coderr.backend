from django.db import models
from offers_app.models import OfferModel, OfferDetails
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

class OrderModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In_progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    offer_detail = models.ForeignKey(OfferDetails, on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    buisness_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_orders')
    title = models.CharField(max_length=50)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    class Meta:
        ordering = ["-created_at"]