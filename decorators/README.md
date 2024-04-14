## decorators

[access_decorator.py](decorators%2Faccess_decorator.py) - В django есть декоратор @login_required который перед выполнением обработчика, проверят авторизован ли пользователь, если нет, то редиректит его на страницу авторизации, данный же декоратор выполняет тот же функционал, но условие, и действие определяете вы сами.
```python
def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_teacher():  # Ваша проверка
                return view_func(request, *args, **kwargs)
        raise Http404()  # Действие если проверка не выполнилась
    return _wrapped_view

path('add-course', teacher_required(CourseCreateView.as_view()), name='create_course'),
```