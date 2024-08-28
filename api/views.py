from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendRequest, User
from .serializers import FriendRequestSerializer, UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({"message": "Login successful", "user": UserSerializer(user).data})  # noqa
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(username__icontains=query)


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user')
        to_user = User.objects.get(id=to_user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='pending').exists(): # noqa
            return Response({"message": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST) # noqa
        friend_request = FriendRequest(from_user=request.user, to_user=to_user, status='pending') # noqa
        friend_request.save()
        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED) # noqa

    def put(self, request, pk):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        serializer = FriendRequestSerializer(friend_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     friend_request = get_object_or_404(FriendRequest, pk=pk)
    #     friend_request.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_requests_to_user = FriendRequest.objects.filter(to_user=user, status='accepted').values_list('from_user', flat=True)
        friend_requests_from_user = FriendRequest.objects.filter(from_user=user, status='accepted').values_list('to_user', flat=True)
        friends = User.objects.filter(Q(id__in=friend_requests_to_user) | Q(id__in=friend_requests_from_user))
        return friends


class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pending_friend_requests = FriendRequest.objects.filter(to_user=user, status='pending').values_list('from_user', flat=True)
        return User.objects.filter(id__in=pending_friend_requests)

print("testing")