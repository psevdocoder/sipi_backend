from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions

REDOC_DESC = 'Проект по СИПИ, 6 семестр. Аналитик - бездельник.'


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
    access_level = 1
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
