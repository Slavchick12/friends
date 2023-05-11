from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .consts import FRIEND_HAS_BEEN_ADDED, INCOMIG, OUTGOING, YOURSELF
from .mixins import FriendsRequestsMixins
from .models import Friends, Notification
from .serializers import FriendsSerializer, NotificationAcceptSerializer, NotificationSerializer


class FriendsViewSet(FriendsRequestsMixins):
    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

    def list(self, request):
        queryset = Friends.objects.filter(Q(first_user=request.user.id) | Q(second_user=request.user.id))
        serializer = FriendsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user_to_delete_id = int(pk)
        current_user_id = request.user.id

        if Friends.objects.filter(first_user=user_to_delete_id, second_user=current_user_id).exists():
            Friends.objects.filter(first_user=user_to_delete_id, second_user=current_user_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if Friends.objects.filter(first_user=current_user_id, second_user=user_to_delete_id).exists():
            Friends.objects.filter(first_user=current_user_id, second_user=user_to_delete_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        queryset = Notification.objects.filter(Q(user_to=request.user) | Q(user_from=request.user))
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        check_user_id = int(pk)
        current_user_id = request.user.id

        if check_user_id == current_user_id:
            return Response({'status': YOURSELF}, status=status.HTTP_200_OK)
        if Notification.objects.filter(user_from=check_user_id, user_to=current_user_id).exists():
            return Response({'status': INCOMIG}, status=status.HTTP_200_OK)
        if Notification.objects.filter(user_from=current_user_id, user_to=check_user_id).exists():
            return Response({'status': OUTGOING}, status=status.HTTP_200_OK)
        if Friends.objects.filter(first_user=current_user_id, second_user=check_user_id).exists() or \
           Friends.objects.filter(first_user=check_user_id, second_user=current_user_id).exists():
            return Response({'status': FRIEND_HAS_BEEN_ADDED}, status=status.HTTP_200_OK)

        return Response({'status': 'No notifications'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk):
        user_to_id = int(pk)
        user_from_id = request.user.id

        notification = get_object_or_404(Notification, user_from=user_from_id, user_to=user_to_id)
        data = {
            'notification': notification,
            'user_to_id': user_to_id,
            'user_from_id': user_from_id
        }
        serializer = NotificationAcceptSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def dismiss(self, request, pk):
        user_to_id = request.user.id
        user_from_id = int(pk)

        notification = get_object_or_404(Notification, user_from=user_from_id, user_to=user_to_id)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
