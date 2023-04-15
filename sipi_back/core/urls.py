from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from core.views import SubjectViewSet, UsersViewSet, \
    QueueViewSet, PollViewSet, VotePollViewSet, \
    AttendanceViewSet, UserCreateViewSet

from sipi_back.redoc import schema_view

router = DefaultRouter()

router.register('subjects', SubjectViewSet, basename='subjects')

router.register('users/create', UserCreateViewSet, basename='create_user')

# router.register('users/me', CurrentUserViewSet, basename='users_me')

router.register('users', UsersViewSet, basename='users')

router.register('polls/vote', VotePollViewSet, basename='poll_vote')

router.register('polls', PollViewSet, basename='polls')

router.register('queue', QueueViewSet, basename='queue')

router.register('attendance', AttendanceViewSet, basename='attendance')


urlpatterns = [
    path('', include(router.urls)),

    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),


    # redoc urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
