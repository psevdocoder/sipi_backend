from rest_framework import mixins, viewsets


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    POST request
    """
    pass


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    GET all items (/items/) or GET specified item (/item/id/)
    """
    pass


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    GET list of items (/item/)
    """
    pass


class DestroyViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    DELETE specified item
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


class ListCreateDestroy(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    POST, GET (/item/), DELETE requests
    """
    pass


class RetrieveListCreateDestroyUpdate(mixins.RetrieveModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      mixins.UpdateModelMixin,
                                      viewsets.GenericViewSet
                                      ):
    """
    POST, GET (/item/ and /item/id/) DELETE, PUT requests
    """
    http_method_names = ['get', 'post', 'put', 'delete']
