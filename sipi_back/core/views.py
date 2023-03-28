from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from core.filters import QueueFilter
from core.mixins import CreateViewSet, GetViewSet, GetListViewSet
from core.permissions import IsAdmin, IsAdminOrAuthRead, IsModerator, \
    HasFilterQueryParam
from core.serializers import UsersCreateSerializer, UsersSerializer, \
    QueueSerializer, PollSerializer, VoteSerializer
from core.models import Subject, Queue, Poll, Choice
from core import serializers
from users.models import User


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Subject operations
    """
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = (IsAdminOrAuthRead,)


class UserCreateViewSet(CreateViewSet):
    """
    Creating new users by admin
    """
    permission_classes = (IsAdmin,)
    serializer_class = UsersCreateSerializer


class UsersViewSet(GetViewSet):
    """
    Get specified user or users list
    """
    serializer_class = UsersSerializer
    permission_classes = (IsModerator,)
    queryset = User.objects.all()


class CurrentUserViewSet(GetListViewSet):
    """
    Get current user info
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UsersSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            return self.request.user
        return super().get_object()


class QueueViewSet(GetListViewSet, CreateViewSet):
    permission_classes = [permissions.IsAuthenticated, HasFilterQueryParam]
    serializer_class = QueueSerializer
    queryset = Queue.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QueueFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class VotePollViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = VoteSerializer
