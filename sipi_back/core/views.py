from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from core.filters import QueueFilter
from core.mixins import CreateViewSet, GetViewSet, GetListViewSet, \
    RetrieveListCreateDestroy
from core.permissions import IsAdmin, IsAdminOrAuthRead, IsModerator, \
    HasFilterQueryParam
from core.serializers import UsersCreateSerializer, UsersSerializer, \
    QueueSerializer, PollSerializer, VoteSerializer, AttendanceSerializer
from core.models import Subject, Queue, Poll, Choice, Attendance
from core import serializers
from users.models import User


class SubjectViewSet(RetrieveListCreateDestroy):
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


class PollViewSet(RetrieveListCreateDestroy):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsModerator]


class VotePollViewSet(CreateViewSet):
    queryset = Choice.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        subject_slug = self.kwargs['subject_slug']
        subject = get_object_or_404(Subject, slug=subject_slug)
        return Attendance.objects.filter(subject=subject)

    def perform_create(self, serializer):
        subject_slug = self.kwargs['subject_slug']
        subject = get_object_or_404(Subject, slug=subject_slug)
        serializer.save(subject=subject)