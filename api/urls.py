from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView, FriendRequestView, FriendsListView, PendingFriendRequestsView # noqa

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'), # noqa
    path('friend-request/<int:pk>/', FriendRequestView.as_view(), name='respond-friend-request'), # noqa
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'), # noqa
]
