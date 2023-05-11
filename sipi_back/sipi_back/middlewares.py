import logging
import datetime
import urllib.parse

from sipi_back.settings import DEBUG

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    import urllib.parse

    def __call__(self, request):
        response = self.get_response(request)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        endpoint = request.path
        method = request.method
        username = request.user.username \
            if request.user.is_authenticated else 'anonymous'
        if DEBUG is True:
            ip_address = request.META.get('REMOTE_ADDR', 'unknown')
        else:
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = remote_addr.split(',')[0].strip() if remote_addr else \
                'unknown'

        # Extracting and logging URL parameters
        params = urllib.parse.urlencode(request.GET) if request.GET else ''
        log_data = f'{time}, {method}: {endpoint}?{params}, ' \
                   f'user: {username}, status code: {response.status_code},' \
                   f' IP: {ip_address}'
        logger.info(log_data)
        return response
