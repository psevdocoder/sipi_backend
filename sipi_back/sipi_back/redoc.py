from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions, status

REDOC_DESC = 'Проект по СИПИ, 6 семестр. Аналитик - бездельник.' \
             '<br>' \
             '<h1> Алгоритм работы с API </h1>' \
             '1. Любой существующий в системе пользователь получает токен' \
             ' авторизации в поле <b>access</b>, отправив POST запрос' \
             ' по эндпоинту <code>/api/auth/jwt/create/</code> ' \
             'с логином и паролем.<br>' \
             '2. Все запросы далее (за исключением упомянутого выше) ' \
             'обрабатываются в соответствии с приведенными ниже примерами ' \
             'только по токену авторизации, переданному в заголовке запроса.'


SECURITY_DEFINITIONS = {
    "BearerAuth": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header"
    }
}


schema_view = get_schema_view(
    openapi.Info(
        title="Group Assistant API",
        default_version='v1',
        description=REDOC_DESC,
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)

access = {
    1: "Пользователь",
    2: "Модератор",
    3: "Администратор"
}


def sipi_redoc(description, operation_id, tag, access_level: int):

    access_list = [access[level] for level in access if level > access_level]
    access_str = ", ".join(access_list)

    return swagger_auto_schema(
        security=[{'Bearer': []}],
        operation_description=f'{description}<br>Права доступа: '
                              f'<b>{access.get(access_level)}<b>'
                              f'{f", {access_str}" if access_str else ""}',
        operation_id=operation_id,
        tags=[tag]
    )


def sipi_redoc_user_me(tag):
    access_level = 1
    access_list = [access[level] for level in access if level > access_level]
    access_str = ", ".join(access_list)

    description = 'Возвращает информацию о своей учетной записи'
    operation_id = 'Получить информацию о себе'

    return swagger_auto_schema(
        security=[{'Bearer': []}],
        operation_description=f'{description}<br>Права доступа: '
                              f'<b>{access.get(access_level)}<b>'
                              f'{f", {access_str}" if access_str else ""}',
        operation_id=operation_id,
        tags=[tag],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'personal_cipher':
                        openapi.Schema(type=openapi.TYPE_STRING),
                    'role': openapi.Schema(type=openapi.TYPE_INTEGER),
                    "user_fullname": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        },
    )


def sipi_queue_access():
    access_level = 2
    access_list = [access[level] for level in access if level > access_level]
    access_str = ", ".join(access_list)

    description = 'Эндпоинт изменяющий разрешающее значение на участие в' \
                  'очереди по предмету'
    operation_id = 'Регулировать возможность встать в очередь'
    tag = 'Предметы'
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'subject_slug': openapi.Schema(type=openapi.TYPE_STRING),
                'is_open': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
            required=['subject_slug', 'is_open']
        ),
        security=[{'Bearer': []}],
        operation_description=f'{description}<br>Права доступа: '
                              f'<b>{access.get(access_level)}<b>'
                              f'{f", {access_str}" if access_str else ""}',
        operation_id=operation_id,
        tags=[tag],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Успешный ответ',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Некорректный запрос',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Предмет не найден',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        },
    )
