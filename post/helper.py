import logging
from redis import Redis

logger = logging.getLogger('django')
redis = Redis(host='10.0.123.45', port=6379)


def log_client_ip(func):
    def wrap(request):
        host = request.get_host()
        logger.info(host)
        return func(request)
    return wrap


def counter(func):
    def wrap(request):
        aid = int(request.GET.get('aid'))
        redis.incr('ARTICLE-%s-COUNTER' % aid)
        ip = request.META['REMOTE_ADDR']
        if redis.sadd('VIEWER-IP', ip):
            redis.incr('IP-COUNTER')
        return func(request)
    return wrap
