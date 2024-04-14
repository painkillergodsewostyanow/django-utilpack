from django.urls.exceptions import Http404


def right_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.has_right():  # Ваша проверка
                return view_func(request, *args, **kwargs)
        raise Http404()  # Действие если проверка не выполнилась
    return _wrapped_view