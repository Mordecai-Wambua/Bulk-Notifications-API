from django.db import transaction
from rest_framework import serializers
from .models import Sender, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'channel']



class SenderSerializer(serializers.ModelSerializer):
    notifications = NotificationSerializer(many=True)

    class Meta:
        model = Sender
        fields = ['name', 'email', 'notifications']

    def validate(self, data):
        if not data.get('notifications'):
            raise serializers.ValidationError(
                'At least one notification is required'
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        notifications_data = validated_data.pop('notifications')
        sender = Sender.objects.create(**validated_data)

        notifications = [
            Notification(sender=sender, **notification_data)
            for notification_data in notifications_data
        ]
        Notification.objects.bulk_create(notifications)
        return sender