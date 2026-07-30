from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SenderSerializer


class NotificationView(APIView):
    def post(self, request):
        serializer = SenderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        sender = serializer.save()

        return Response(
            {
                "message": "Sender and notifications created successfully.",
                "sender_id": sender.id,
                "notifications_created": sender.notifications.count(),
            },
            status=status.HTTP_201_CREATED,
        )
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
