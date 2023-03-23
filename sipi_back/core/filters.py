import django_filters
from django_filters import filters


class QueueFilter(django_filters.FilterSet):
    subject = filters.CharFilter(
        field_name='subject__slug',
        lookup_expr='exact',
    )
