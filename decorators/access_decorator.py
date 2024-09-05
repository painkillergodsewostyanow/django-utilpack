from functools import wraps
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.urls.exceptions import Http404


def right_required(condition: Callable[[HttpRequest], bool], if_hasnt: Callable):
    def _right_required(view_func):
        @wraps(view_func)
        def _wrapped_view(request: HttpRequest, *args, **kwargs):
            if condition(request, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            if_hasnt(request)  # Действие если проверка не выполнилась

        return _wrapped_view

    return _right_required
