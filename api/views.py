# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from .serializers import UserSerializer, LocationSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Location
from rest_framework.decorators import action
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Extract user data from request
        user_data = self.request.data
        username = user_data.get('username')
        email = user_data.get('email')
        mobile_num = user_data.get('mobile_num')
       
        # Check if the username, email, or mobile number already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'A user with this Mobile Number already exists.'})

        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})

        
        # Save the user and profile
        serializer.save()

class UpdateLocationView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Disable authentication

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')
        location_name = request.data.get('location')
        
        if not user_id or not location_name:
            return Response(
                {"error": "User ID and location are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
            location, created = Location.objects.update_or_create(
                user=user,
                defaults={'location': location_name}
            )
            return Response({'message': 'Location updated successfully'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class GetLocationView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Disable authentication

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')

        if not user_id:
            return Response(
                {"error": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
            location = Location.objects.get(user=user)
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Location.DoesNotExist:
            return Response({'error': 'Location does not exist for this user'}, status=status.HTTP_404_NOT_FOUND)