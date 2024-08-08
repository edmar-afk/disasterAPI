from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location']
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
      
        user = User.objects.create_user(**validated_data)
        return user
    

