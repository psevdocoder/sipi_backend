from rest_framework import mixins, viewsets


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    POST request
    """
    pass


class GetViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    GET all items (/items/) or GET specified item (/item/1/)
    """
    pass
