from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import FriendsViewSet, NotificationViewSet

router_v1 = DefaultRouter()
router_v1.register('notifications', NotificationViewSet, basename='notifications')
router_v1.register('friends', FriendsViewSet, basename='friends')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
]
