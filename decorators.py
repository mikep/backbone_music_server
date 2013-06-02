from functools import wraps
from django.http import HttpResponse

import json
import logging

log = logging.getLogger(__name__)


def is_authorized():
    def _decorate(fn):
        @wraps(fn)
        def _new_fn(request, *args, **kwargs):
            if 'user' not in request.session:
                return HttpResponse(status=401)
            else:
                if json.loads(request.session.get('user')).get('role') == 'user':
                    return fn(request, *args, **kwargs)
                return HttpResponse(status=403)

        return _new_fn
    return _decorate

