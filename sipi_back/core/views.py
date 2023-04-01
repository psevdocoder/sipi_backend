from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.filters import BySubjectFilter
from core.mixins import CreateViewSet, RetrieveListViewSet, ListViewSet, \
    RetrieveListCreateDestroy
from core.permissions import IsAdmin, IsAdminOrAuthRead, IsModerator, \
    HasFilterQueryParam, IsModeratorOrAuthRead
from core.serializers import UsersCreateSerializer, UsersSerializer, \
    QueueSerializer, PollSerializer, VoteSerializer, AttendanceSerializer
from core.models import Subject, Queue, Poll, Choice, Attendance
from core import serializers
from users.models import User


class SubjectViewSet(RetrieveListCreateDestroy):
    """
    Subject management
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


class UsersViewSet(RetrieveListViewSet):
    """
    Get specified user or users list
    """
    serializer_class = UsersSerializer
    permission_classes = (IsModerator,)
    queryset = User.objects.all()


class CurrentUserViewSet(ListViewSet):
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


class QueueViewSet(ListViewSet, CreateViewSet):
    """
    ViewSet for Queue functionality for existing Subject
    """
    permission_classes = [permissions.IsAuthenticated, HasFilterQueryParam]
    serializer_class = QueueSerializer
    queryset = Queue.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BySubjectFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PollViewSet(RetrieveListCreateDestroy):
    """
    ViewSet providing Polls management
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsModerator]


class VotePollViewSet(CreateViewSet):
    """
    ViewSet for choosing specified vote
    """
    queryset = Choice.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet used for marking attendance of students
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsModeratorOrAuthRead, HasFilterQueryParam]
    filterset_class = BySubjectFilter

    # def get_queryset(self):
    #     subject = self.kwargs['subject']
    #     subject = get_object_or_404(Subject, slug=subject)
    #     return Attendance.objects.filter(subject=subject)
    #
    # def perform_create(self, serializer):
    #     subject = self.kwargs['subject']
    #     subject = get_object_or_404(Subject, slug=subject)
    #     serializer.save(subject=subject)
