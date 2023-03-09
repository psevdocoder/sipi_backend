from http import HTTPStatus

import requests
from rest_framework import viewsets, permissions
from rest_framework.request import Request

from core.mixins import CreateViewSet, GetViewSet, GetItemViewSet
from core.permissions import IsAdmin, IsAdminOrAuthRead, IsModerator
from core.serializers import UsersCreateSerializer, UsersSerializer, \
    JoinLeftQueueSerializer
from core.models import Subject, Queue
from core import serializers
from users.models import User
from rest_framework.response import Response


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


class CurrentUserViewSet(GetItemViewSet):
    """
    Get current user info
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UsersSerializer

    def get_queryset(self):
        user = User.objects.filter(username=self.request.user)
        print(user)
        return user

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            print(self.request.user)
            return self.request.user
        return super(CurrentUserViewSet, self).get_object()


class QueueViewSet(viewsets.ModelViewSet):
    serializer_class = JoinLeftQueueSerializer
    queryset = Queue.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
