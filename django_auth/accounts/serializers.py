from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class RegisterSerializer (serializers.ModelSerializer): # Converts the User model into JSON using serializers
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())] # To prevent duplicate emails
    )
    password = serializers.CharField(write_only=True, min_length=8) # Write_only = True so we do NOT return the password in API responses

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user