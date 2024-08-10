from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('update-location/', views.UpdateLocationView.as_view(), name='update-location'),
    path('get-location/', views.GetLocationView.as_view(), name='get-location'),
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    
    # Add the alert endpoint
    path('create-alert/', views.AlertCreateView.as_view(), name='create-alert'),
    path('latest-alert/', views.LatestAlertView.as_view(), name='latest-alert'),
    path('get-alerts/', views.get_alerts, name='get_alerts'),  # Optional: endpoint for fetching alerts
    path('api/check-alerts/', views.check_alerts, name='check_alerts'),
]
