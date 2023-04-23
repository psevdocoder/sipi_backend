from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.filters import BySubjectFilter
from core.mixins import CreateViewSet, RetrieveListViewSet, ListViewSet, \
    RetrieveListCreateDestroy, RetrieveListCreateDestroyUpdate
from core.permissions import IsAdmin, IsAdminOrAuthRead, \
    HasFilterQueryParamOrUnsafeMethod, IsModeratorOrAuthRead
from core.serializers import UsersSerializer, QueueSerializer, PollSerializer,\
    VoteSerializer, AttendanceSerializer, UsersCreateSerializer
from core.models import Subject, Queue, Poll, Choice, Attendance
from core import serializers
from sipi_back.redoc import sipi_redoc, sipi_redoc_user_me
from users.models import User


class SubjectViewSet(RetrieveListCreateDestroy):
    """
    Класс предоставляющий управление предметами
    """
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = (IsAdminOrAuthRead,)

    REDOC_TAG = 'Предметы'

    LIST_DESCRIPTION = 'Получить список предметов'
    LIST_OPERATION_ID = 'Получить список предметов'

    CREATE_DESCRIPTION = 'Создать предмет'
    CREATE_OPERATION_ID = 'Создать предмет'

    RETRIEVE_DESCRIPTION = 'Получить предмет по ID'
    RETRIEVE_OPERATION_ID = 'Получить предмет по ID'

    DESTROY_DESCRIPTION = 'Удалить предмет'
    DESTROY_OPERATION_ID = 'Удалить предмет'

    @sipi_redoc(description=LIST_DESCRIPTION, access_level=1,
                operation_id=LIST_OPERATION_ID, tag=REDOC_TAG)
    def list(self, request, *args, **kwargs):
        """
        Получить список предметов
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=CREATE_DESCRIPTION,
                operation_id=CREATE_OPERATION_ID,
                access_level=2, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Создать новый предмет.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION, access_level=1,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить сведения о конкретном предмете
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().retrieve(request, *args, **kwargs)

    @sipi_redoc(description=DESTROY_DESCRIPTION, access_level=1,
                operation_id=DESTROY_OPERATION_ID, tag=REDOC_TAG)
    def destroy(self, request, *args, **kwargs):
        """
        Удалить предмет
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().destroy(request, *args, **kwargs)


class UserCreateViewSet(CreateViewSet):
    """
    Вьюсет обеспечивающий создание пользователей
    """
    permission_classes = (IsAdmin,)
    serializer_class = UsersCreateSerializer

    REDOC_TAG = 'Пользователи'

    CREATE_DESCRIPTION = 'Создать нового пользователя'
    CREATE_OPERATION_ID = 'Создать пользователя'

    @sipi_redoc(description=CREATE_DESCRIPTION, access_level=3,
                operation_id=CREATE_OPERATION_ID, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Создать пользователя
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().create(request, *args, **kwargs)


class UsersViewSet(RetrieveListViewSet):
    """
    Вьюсет для получения пользователей или пользователя
    """
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    REDOC_TAG = 'Пользователи'

    LIST_DESCRIPTION = 'Возвращает список пользователей'
    LIST_OPERATION_ID = 'Получить список пользователей'

    RETRIEVE_DESCRIPTION = 'Получить сведения о пользователе'
    RETRIEVE_OPERATION_ID = 'Просмотреть пользователя'

    @action(detail=False, methods=['get'], url_path='me')
    @sipi_redoc_user_me(tag=REDOC_TAG)
    def me(self, request):
        """
        Получить информацию о своем профиле
        :param request:
        :return:
        """
        if not request.data:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @sipi_redoc(description=LIST_DESCRIPTION,
                operation_id=LIST_OPERATION_ID, tag=REDOC_TAG, access_level=1)
    def list(self, request, *args, **kwargs):
        """
        Получить список пользователей
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG,
                access_level=1)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить сведения о пользователе
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().retrieve(request, *args, **kwargs)


class QueueViewSet(ListViewSet, CreateViewSet):
    """
    Вьюсет для функционирования очередей в существующих предметах Subject
    """
    permission_classes = [
        permissions.IsAuthenticated, HasFilterQueryParamOrUnsafeMethod]
    serializer_class = QueueSerializer
    queryset = Queue.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BySubjectFilter

    REDOC_TAG = 'Очереди'

    LIST_DESCRIPTION = 'Получить список людей в очереди по slug предмета. ' \
                       'Например: /api/queue/?subject=ost'
    LIST_OPERATION_ID = 'Получить список людей в очереди'

    CREATE_DESCRIPTION = 'Встать в очередь'
    CREATE_OPERATION_ID = 'Встать в очередь'

    def perform_create(self, serializer):
        """
        Изменение перед сохранением
        :param serializer:
        :return:
        """
        serializer.save(user=self.request.user)

    @sipi_redoc(description=CREATE_DESCRIPTION, access_level=1,
                operation_id=CREATE_OPERATION_ID, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Встать в очереди
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=LIST_DESCRIPTION, access_level=1,
                operation_id=LIST_OPERATION_ID, tag=REDOC_TAG)
    def list(self, request, *args, **kwargs):
        """
        Список людей в очереди
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().list(request, *args, **kwargs)


class PollViewSet(RetrieveListCreateDestroy):
    """
    ViewSet providing Polls management
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsModeratorOrAuthRead]

    REDOC_TAG = 'Опросы'

    LIST_DESCRIPTION = 'Получить список опросов'
    LIST_OPERATION_ID = 'Получить список опросов'

    CREATE_DESCRIPTION = 'Создать опрос'
    CREATE_OPERATION_ID = 'Создать опрос'

    RETRIEVE_DESCRIPTION = 'Получить опрос по ID'
    RETRIEVE_OPERATION_ID = 'Получить опрос по ID'

    DESTROY_DESCRIPTION = 'Удалить опрос'
    DESTROY_OPERATION_ID = 'Удалить опрос'

    @sipi_redoc(description=LIST_DESCRIPTION, access_level=1,
                operation_id=LIST_OPERATION_ID, tag=REDOC_TAG)
    def list(self, request, *args, **kwargs):
        """
        Список опросов
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=CREATE_DESCRIPTION,
                operation_id=CREATE_OPERATION_ID,
                access_level=2, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Создать опрос
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION, access_level=1,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию об опросе
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().retrieve(request, *args, **kwargs)

    @sipi_redoc(description=DESTROY_DESCRIPTION, access_level=1,
                operation_id=DESTROY_OPERATION_ID, tag=REDOC_TAG)
    def destroy(self, request, *args, **kwargs):
        """
        Удалить опрос
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().destroy(request, *args, **kwargs)


class VotePollViewSet(CreateViewSet):
    """
    ViewSet for choosing specified vote
    """
    queryset = Choice.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    REDOC_TAG = 'Опросы'

    CREATE_DESCRIPTION = 'Оставить свой голос в опросе'
    CREATE_OPERATION_ID = 'Проголосовать'

    @sipi_redoc(description=CREATE_DESCRIPTION, access_level=1,
                operation_id=CREATE_OPERATION_ID, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Проголосовать в опросе
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().create(request, *args, **kwargs)


class AttendanceViewSet(RetrieveListCreateDestroyUpdate):
    """
    ViewSet used for marking attendance of students
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsModeratorOrAuthRead,
                          HasFilterQueryParamOrUnsafeMethod]
    filterset_class = BySubjectFilter

    REDOC_TAG = 'Посещаемость'

    LIST_DESCRIPTION = 'Нужен параметр фильтра по slug предмета. ' \
                       'Например: /api/attendance/?subject=ost <br>' \
                       'Параметр lesson_serial_number - Порядковый номер ' \
                       'пары, урока и т.д.'
    LIST_OPERATION_ID = 'Получение посещаемости студентов'

    CREATE_DESCRIPTION = 'Поставить отметку о посещаемости студента.  <br>' \
                         'Параметр lesson_serial_number - Порядковый номер ' \
                         'пары, урока и т.д.'
    CREATE_OPERATION_ID = 'Поставить посещение студенту'

    RETRIEVE_DESCRIPTION = 'Поставить отметку о посещаемости студента. <br>' \
                           'Параметр lesson_serial_number - Порядковый номер '\
                           'пары, урока и т.д.'
    RETRIEVE_OPERATION_ID = 'Поставить посещение студенту'

    UPDATE_DESCRIPTION = 'Изменить отметку посещения студенту.  <br>' \
                         'Параметр lesson_serial_number - Порядковый номер ' \
                         'пары, урока и т.д.'
    UPDATE_OPERATION_ID = 'Изменить посещение студенту'

    DESTROY_DESCRIPTION = 'Удалить отметку о посещаемости. <br>' \
                          'Параметр lesson_serial_number - Порядковый номер ' \
                          'пары, урока и т.д.'
    DESTROY_OPERATION_ID = 'Удалить отметку о посещаемости'

    @sipi_redoc(description=LIST_DESCRIPTION, access_level=1,
                operation_id=LIST_OPERATION_ID, tag=REDOC_TAG)
    def list(self, request, *args, **kwargs):
        """
        Список посещаемости
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=CREATE_DESCRIPTION, access_level=2,
                operation_id=CREATE_OPERATION_ID, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Создать отметку о посещаемости студента
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION, access_level=1,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию о конкретном пользователе в конкретный день
        по конкретному предмету
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().retrieve(request, *args, **kwargs)

    @sipi_redoc(description=UPDATE_DESCRIPTION, access_level=2,
                operation_id=UPDATE_OPERATION_ID, tag=REDOC_TAG)
    def update(self, request, *args, **kwargs):
        """
        Изменить информацию о конкретном пользователе в конкретный день
        по конкретному предмету
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().update(request, *args, **kwargs)

    @sipi_redoc(description=DESTROY_DESCRIPTION, access_level=1,
                operation_id=DESTROY_OPERATION_ID, tag=REDOC_TAG)
    def destroy(self, request, *args, **kwargs):
        """
        Удалить информацию о конкретном пользователе в конкретный день
        по конкретному предмету
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().destroy(request, *args, **kwargs)
