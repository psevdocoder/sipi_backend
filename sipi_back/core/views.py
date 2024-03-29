from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.filters import BySubjectFilter
from core.mixins import CreateViewSet, RetrieveListViewSet, \
    RetrieveListCreateDestroy, RetrieveListCreateDestroyUpdate, \
    ListCreateDestroy
from core.permissions import IsAdmin, IsAdminOrAuthRead, \
    HasFilterQueryParamOrUnsafeMethod, IsModeratorOrAuthRead, IsModerator
from core.serializers import UsersSerializer, QueueSerializer, PollSerializer,\
    VoteSerializer, AttendanceSerializer, UsersCreateSerializer
from core.models import Subject, Queue, Poll, Choice, Attendance
from core import serializers
from sipi_back.redoc import sipi_redoc, sipi_redoc_user_me, \
    sipi_queue_access, queue_list_filtered
from users.models import User


class SubjectViewSet(RetrieveListCreateDestroy):
    """
    Subject management
    """
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = (IsAdminOrAuthRead,)
    lookup_field = 'slug'

    REDOC_TAG = 'Предметы'

    LIST_DESCRIPTION = 'Получить список предметов'
    LIST_OPERATION_ID = 'Получить список предметов'

    CREATE_DESCRIPTION = 'Создать предмет'
    CREATE_OPERATION_ID = 'Создать предмет'

    RETRIEVE_DESCRIPTION = 'Получить предмет по ID'
    RETRIEVE_OPERATION_ID = 'Получить предмет по ID'

    DESTROY_DESCRIPTION = 'Удалить предмет'
    DESTROY_OPERATION_ID = 'Удалить предмет'

    MODIFY_QUEUE_ERR = 'subject_slug and is_open fields are both required ' \
                       'with declared types.'

    @sipi_redoc(description=LIST_DESCRIPTION, access_level=1,
                operation_id=LIST_OPERATION_ID, tag=REDOC_TAG)
    def list(self, request, *args, **kwargs):
        """
        Получить информацию о всех предметах.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода list родительского класса
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=CREATE_DESCRIPTION,
                operation_id=CREATE_OPERATION_ID,
                access_level=2, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Создать предмет.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода create родительского класса
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION, access_level=1,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить пользователя по slug.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода retrieve родительского класса
        """
        return super().retrieve(request, *args, **kwargs)

    @sipi_redoc(description=DESTROY_DESCRIPTION, access_level=1,
                operation_id=DESTROY_OPERATION_ID, tag=REDOC_TAG)
    def destroy(self, request, *args, **kwargs):
        """
        Обработать удаление предмета.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода destroy родительского класса
        """
        return super().destroy(request, *args, **kwargs)

    @action(methods=['POST'], permission_classes=[IsModerator],
            detail=False, url_path='access')
    @sipi_queue_access()
    def modify_queue_access(self, request):
        """
        Обработать изменение статуса предмета
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :return: Response: Статус обработки запроса
        """
        subject_slug = request.data.get('subject_slug')
        is_open = request.data.get('is_open')

        if not all([isinstance(subject_slug, str), isinstance(is_open, bool)]):
            return Response({'error': self.MODIFY_QUEUE_ERR},
                            status=status.HTTP_400_BAD_REQUEST)

        subject = get_object_or_404(Subject, slug=subject_slug)
        subject.is_open = is_open
        subject.save()
        return Response({'success': f'Subject with slug {subject_slug} '
                                    f'updated successfully.'})


class UserCreateViewSet(CreateViewSet):
    """
    Creating new users by admin
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
        Обработать создание пользователя
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода create родительского класса
        """
        return super().create(request, *args, **kwargs)


class UsersViewSet(RetrieveListViewSet):
    """
    Get specified user or users list
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
        Вернуть информацию о пользователе
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :return: Response: Информация о пользователе
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
        Получить информацию о всех пользователях.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода list родительского класса
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG,
                access_level=1)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить пользователя по id.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода retrieve родительского класса
        """
        return super().retrieve(request, *args, **kwargs)


class QueueViewSet(ListCreateDestroy):
    """
    ViewSet for Queue functionality for existing Subject
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QueueSerializer
    queryset = Queue.objects.all()
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'slug'

    REDOC_TAG = 'Очереди'

    LIST_DESCRIPTION = 'Получить список людей в очереди по slug предмета. ' \
                       'Например: /api/queue/?subject=ost'
    LIST_OPERATION_ID = 'Получить список людей в очереди'

    CREATE_DESCRIPTION = 'Встать в очередь'
    CREATE_OPERATION_ID = 'Встать в очередь'

    DESTROY_DESCRIPTION = 'Выйти из очереди'
    DESTROY_OPERATION_ID = 'Выйти из очереди'

    def perform_create(self, serializer):
        """
        Выполнить добавление в очередь
        :param serializer: Сериализатор, используемый для десериализации и
        проверки данных.
        :return: None
        """
        subject = serializer.validated_data['subject']
        if not subject.is_open:
            raise serializers.ValidationError(
                'Cannot add to queue for a closed subject.')
        serializer.save(user=self.request.user)

    @sipi_redoc(description=CREATE_DESCRIPTION, access_level=1,
                operation_id=CREATE_OPERATION_ID, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Обработать добавление в очередь.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода create родительского класса
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=LIST_DESCRIPTION, access_level=1,
                operation_id=LIST_OPERATION_ID, tag=REDOC_TAG)
    def list(self, request, *args, **kwargs):
        """
        Получить очередь по всем предметам.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода list родительского класса
        """
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='filtered')
    @queue_list_filtered()
    def list_filtered(self, request):
        """
        Получить очередь по предмету
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :return: Response
        """
        slug = self.request.query_params.get('subject', None)
        if not slug:
            message = {"error": "incorrect filter param"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        subject = get_object_or_404(Subject, slug=slug)
        queryset = self.filter_queryset(self.get_queryset())
        queue_items = queryset.filter(subject__slug=slug)
        serializer = QueueSerializer(queue_items, many=True)
        data = {"is_open": subject.is_open, "subject_name": subject.title, "queue_persons": serializer.data}
        return Response(data)

    @sipi_redoc(description=DESTROY_DESCRIPTION, access_level=1,
                operation_id=DESTROY_OPERATION_ID, tag=REDOC_TAG)
    def destroy(self, request, *args, **kwargs):
        """
        Обработать выход из очереди.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода destroy родительского класса
        """
        subject_slug = kwargs.get('slug')
        queryset = self.filter_queryset(self.get_queryset())
        queue_item = get_object_or_404(queryset, subject__slug=subject_slug,
                                       user=request.user)
        queue_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        Получить список опросов.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода list родительского класса
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=CREATE_DESCRIPTION,
                operation_id=CREATE_OPERATION_ID,
                access_level=2, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Создать опрос.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода create родительского класса
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION, access_level=1,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить опрос по id.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода retrieve родительского класса
        """
        return super().retrieve(request, *args, **kwargs)

    @sipi_redoc(description=DESTROY_DESCRIPTION, access_level=1,
                operation_id=DESTROY_OPERATION_ID, tag=REDOC_TAG)
    def destroy(self, request, *args, **kwargs):
        """
        Убрать опрос по id.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода destroy родительского класса
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
        Обработать запрос на голосование пользователя.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода create родительского класса
        """
        return super().create(request, *args, **kwargs)


class AttendanceViewSet(RetrieveListCreateDestroyUpdate):
    """
    Вьюсет обрабатывающий запросы по посещаемости.
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

    RETRIEVE_DESCRIPTION = 'Получить отметку о посещаемости студента.'
    RETRIEVE_OPERATION_ID = 'Получить посещение студента'

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
        Получить список посещаемости по фильтру предмета.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода list родительского класса
        """
        return super().list(request, *args, **kwargs)

    @sipi_redoc(description=CREATE_DESCRIPTION, access_level=2,
                operation_id=CREATE_OPERATION_ID, tag=REDOC_TAG)
    def create(self, request, *args, **kwargs):
        """
        Создать отметку о посещаемости.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода create родительского класса
        """
        return super().create(request, *args, **kwargs)

    @sipi_redoc(description=RETRIEVE_DESCRIPTION, access_level=1,
                operation_id=RETRIEVE_OPERATION_ID, tag=REDOC_TAG)
    def retrieve(self, request, *args, **kwargs):
        """
        Получить отметку о посещаемости по id.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода retrieve родительского класса
        """
        return super().retrieve(request, *args, **kwargs)

    @sipi_redoc(description=UPDATE_DESCRIPTION, access_level=2,
                operation_id=UPDATE_OPERATION_ID, tag=REDOC_TAG)
    def update(self, request, *args, **kwargs):
        """
        Обновить отметку о посещаемости по id.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода retrieve родительского класса
        """
        return super().update(request, *args, **kwargs)

    @sipi_redoc(description=DESTROY_DESCRIPTION, access_level=2,
                operation_id=DESTROY_OPERATION_ID, tag=REDOC_TAG)
    def destroy(self, request, *args, **kwargs):
        """
        Убрать отметку о посещаемости по id.
        :param request: Объект запроса, содержащий данные о запросе клиента.
        :param args:  Представляет необязательные позиционные аргументы.
        :param kwargs: Представляет необязательные именованные аргументы.
        :return: Возвращает результат метода destroy родительского класса
        """
        return super().destroy(request, *args, **kwargs)
