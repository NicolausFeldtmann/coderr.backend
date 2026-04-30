from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from offers_app.models import OfferModel
from .serializers import OfferSerializer, OfferListSerializer
from .permissions import IsOwnerOrAdmin

class OfferListView(generics.ListCreateAPIView):
    queryset = OfferModel.objects.prefetch_related('details').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferListSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfferModel.objects.prefetch_related("details").all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = OfferSerializer