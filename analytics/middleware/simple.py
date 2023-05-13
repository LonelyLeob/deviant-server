from django.http import HttpRequest


class SimpleMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response
    
    def _process_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip