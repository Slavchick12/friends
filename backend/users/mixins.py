from rest_framework import mixins, viewsets


class FriendsRequestsMixins(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass
