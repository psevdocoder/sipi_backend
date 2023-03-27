from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from core.views import SubjectViewSet, UserCreateViewSet, UsersViewSet, \
    CurrentUserViewSet, QueueViewSet, PollViewSet, VotePollViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()

router.register('subjects', SubjectViewSet, basename='subjects')

router.register('users/create', UserCreateViewSet, basename='create_user')

router.register('users/me', CurrentUserViewSet, basename='users_me')

router.register('users', UsersViewSet, basename='users')

router.register('polls/vote', VotePollViewSet, basename='poll_vote')

router.register('polls', PollViewSet, basename='polls')

router.register('queue', QueueViewSet, basename='queue')

schema_view = get_schema_view(
   openapi.Info(
      title="Group Assistant API",
      default_version='v1',
      description="Test description",
      # terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('', include(router.urls)),

    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('queue/', QueueViewSet.as_view(), name='queue-list-create'),


    # redoc urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
