from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

BLOCKIP = [
    '192.168.0.4'
]


class BlockIP(MiddlewareMixin):
    @staticmethod
    def is_blocked_ip(ip):
        return ip in BLOCKIP

    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        if self.is_blocked_ip(ip):
            return render(request, 'blockers.html')
        return
