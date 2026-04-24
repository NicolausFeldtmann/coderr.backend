from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers
from user_auth_app.models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            "id", 
            "user", 
            "username", 
            "first_name", 
            "last_name", 
            "location", 
            "tel", 
            "description", 
            "role", 
            "email", 
            "created_at"
        ]

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True,default="")
    last_name = serializers.CharField(required=False, allow_blank=True, default="")
    type = serializers.ChoiceField(choices=[("customer", "Customer"), ("business", "Business")], default="customer")

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError({"error": "Invalid email."})

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError({"error": "Email already exists."})
        return value

    def validate(self, data):
        if data.get("password") != data.get("repeated_password"):
            raise serializers.ValidationError({"error": "Passwords don't match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("repeated_password", None)
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        role = validated_data.pop("type", "customer")

        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, username=username, first_name=first_name, last_name=last_name, email=email, role=role)
        return user

class UsernameAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "invalid access"})
        if not user.check_password(password):
            raise serializers.ValidationError({"error": "invalid access"})

        attrs["user"] = user
        return attrs