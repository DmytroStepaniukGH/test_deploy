from django.urls import path

from notifications.views import NotificationsListView, CountUnreadNotificationsView, UnreadNotificationsListView, ToggleNotificationStatus


urlpatterns = [
    path('all-notifications/', NotificationsListView.as_view(), name='notifications'),
    path('count-unread-notifications/', CountUnreadNotificationsView.as_view(), name='count-unread-notifications'),
    path('unread-notifications/', UnreadNotificationsListView.as_view(), name='unread-notifications'),
    path('toggle-status/<int:notification_id>/', ToggleNotificationStatus.as_view(), name='toggle-status'),
    ]