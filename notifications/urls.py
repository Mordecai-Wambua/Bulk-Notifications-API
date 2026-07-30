from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('notifications/bulk/', NotificationView.as_view(), name='bulk_notification')
]