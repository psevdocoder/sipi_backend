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
    GET all items (/items/) or GET specified item (/item/id/)
    """
    pass


class GetListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    GET list of items (/item/)
    """
    pass


class RetrieveListCreateDestroy(mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet
                                ):
    """
    POST, GET (/item/ and /item/id/) DELETE requests
    """
    pass
