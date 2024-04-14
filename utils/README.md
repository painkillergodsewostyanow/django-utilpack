## utils:

[is_mobile.py](is_mobile.py) - Используя информацию из HTTP_USER_AGENT определяет устройство пользователя
```python
def view(request):
    print(is_mobile(request))
```
