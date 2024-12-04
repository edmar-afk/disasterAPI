# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from .serializers import UserSerializer, LocationSerializer, AlertSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Location, Alert
from rest_framework.decorators import action,api_view
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse
import requests
from django.conf import settings

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
            raise ValidationError({'username': 'A user with this Email already exists.'})

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
        



class AlertCreateView(generics.CreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        alert = serializer.save()

        # Prepare notification content
        notification_content = (
            f"New Alert: {alert.alert_type} in {alert.location}\n\n"
            f"Description:\n{alert.description}"
        )

        # Prepare OneSignal notification payload
        notification_data = {
            "app_id": settings.ONESIGNAL_APP_ID,
            "included_segments": ["All"],
            "contents": {"en": notification_content},
            "headings": {"en": "New Alert From Lakewood Disaster App"},
            "data": {
                "alert_type": alert.alert_type,
                "location": alert.location,
                "description": alert.description,
                "date": str(alert.date)
            },
            "android": {
                "big_picture": alert.image.url if alert.image else None,
            },
            "ios": {
                "big_picture": alert.image.url if alert.image else None,
            },
        }

        # Send notification to OneSignal
        headers = {
            "Authorization": f"Basic {settings.ONESIGNAL_API_KEY}",
            "Content-Type": "application/json; charset=utf-8",
        }
        response = requests.post("https://onesignal.com/api/v1/notifications", json=notification_data, headers=headers)

        # Debug response
        print(response.json())  # Print the response from OneSignal

        return JsonResponse({"message": "Alert created successfully."}, status=201)
    

# View to get all alerts
def get_alerts(request):
    alerts = Alert.objects.all().order_by('-date')
    data = [{"alert_type": alert.alert_type, "location": alert.location,
             "description": alert.description, "date": alert.date} for alert in alerts]
    return JsonResponse(data, safe=False)


class LatestAlertView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Disable authentication

    def get(self, request):
        latest_alert = Alert.objects.all().order_by('-date').first()
        if latest_alert:
            serializer = AlertSerializer(latest_alert)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No alerts found."}, status=status.HTTP_404_NOT_FOUND)
    
def check_alerts(request):
    # Get the timestamp from query parameters (or use a default value)
    last_check = request.GET.get('last_check', None)

    if last_check:
        try:
            last_check_datetime = timezone.datetime.fromisoformat(last_check)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
    else:
        last_check_datetime = timezone.now() - timedelta(minutes=10)  # Default to 10 minutes ago

    # Fetch alerts created after the last check time
    alerts = Alert.objects.filter(date__gte=last_check_datetime).order_by('-date')

    # Convert to a list of dictionaries
    data = [
        {
            'alert_type': alert.alert_type,
            'location': alert.location,
            'description': alert.description,
            'date': alert.date.isoformat()
        }
        for alert in alerts
    ]

    return JsonResponse(data, safe=False)