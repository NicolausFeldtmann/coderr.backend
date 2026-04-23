from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, UsernameAuthSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "role": getattr(user.userprofile, "role", None),
                "user_id": user.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serialier_class = UsernameAuthSerializer

    def post(self, request):
        serializer = self.serialier_class(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, create = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }
        else:
            return Response({"error": "Wrong username or password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)
