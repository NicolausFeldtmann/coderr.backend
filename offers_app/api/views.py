from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from offers_app.models import OfferModel
from .serializers import OfferSerializer

class OfferListView(generics.ListCreateAPIView):
    queryset = OfferModel.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)