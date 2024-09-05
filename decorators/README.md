## decorators

[access_decorator.py](access_decorator.py) - В django есть декоратор @login_required который перед выполнением обработчика, проверят авторизован ли пользователь, если нет, то редиректит его на страницу авторизации, данный же декоратор выполняет тот же функционал, но условие, и действие определяете вы сами. За идею по улучшению спасибо [AspirantDrago](https://github.com/AspirantDrago)

```python
from access_decorator import right_required


def teacher_required(request, *args, **kwargs):
    if request.user.is_authenticated:
        return request.user.is_teacher()


def r_404(request, *args, **kwargs):
    raise Http404()


@right_required(teacher_required, r_404)
def view(request):
    ...

# OR

path(
    'update-course/<int:course_id>',
    right_required(teacher_req, r_404)(ViewClass.as_view()),
     name='update_course'
),
```