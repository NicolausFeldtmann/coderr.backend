from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from offers_app. models import OfferModel, OfferDetails
from .serializers import OfferSerializer, DetailSerializer

class OfferListView(generics.ListCreateAPIView):
    queryset = OfferModel.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

