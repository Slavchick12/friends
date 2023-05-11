from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .consts import FRIEND_HAS_BEEN_ADDED, FRIEND_YOURSELF, NOTIFICATION_SENT
from .models import Friends, Notification, User


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ('first_user', 'second_user')
        read_only_fields = ('first_user', 'second_user')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user_to', 'user_from')
        read_only_fields = ('user_from',)

    def validate(self, data):
        user_to_id = self.initial_data.get('user_to')
        user_from = self.context.get('request').user
        user_from_id = user_from.id

        if user_to_id == user_from_id:
            raise ValidationError(FRIEND_YOURSELF)

        if Notification.objects.filter(user_from=user_from_id, user_to=user_to_id).exists():
            raise ValidationError(NOTIFICATION_SENT)

        if Friends.objects.filter(first_user=user_to_id, second_user=user_from_id).exists() or \
           Friends.objects.filter(first_user=user_from_id, second_user=user_to_id).exists():
            raise ValidationError(FRIEND_HAS_BEEN_ADDED)

        data['user_to_id'] = user_to_id
        data['user_from_id'] = user_from_id
        data['user_from'] = user_from

        return super().validate(data)

    def save(self):
        user_to_id = self.validated_data['user_to_id']
        user_from_id = self.validated_data['user_from_id']
        user_to = self.validated_data['user_to']
        user_from = self.validated_data['user_from']

        if Notification.objects.filter(user_from=user_to_id, user_to=user_from_id).exists():
            Notification.objects.filter(user_from=user_to_id, user_to=user_from_id).delete()
            Friends.objects.create(first_user=user_to, second_user=user_from)
            return

        data = {'user_to': user_to, 'user_from': user_from}
        super().create(data)


class NotificationAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user_to', 'user_from')
        read_only_fields = ('user_to', 'user_from')

    def save(self):
        user_to_id = self.initial_data.get('user_to_id')
        user_from_id = self.initial_data.get('user_from_id')
        user_to = User.objects.get(id=user_to_id)
        user_from = User.objects.get(id=user_from_id)

        Notification.objects.filter(user_from=user_from_id, user_to=user_to_id).delete()
        Friends.objects.create(first_user=user_to, second_user=user_from)
