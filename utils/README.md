## utils:

[is_mobile.py](is_mobile.py) - Используя информацию из HTTP_USER_AGENT определяет устройство пользователя
```python
def view(request):
    print(is_mobile(request))
```
[get_client_ip.py](get_client_ip.py) - Используя информацию из requests получает ip-address клиента
```python
def view(request):
    print(get_client_ip(request))
```
[check_ip.py](check_ip.py) - Содержит две функции, первая проверяет, совпадает ли ip-address с маской, вторая проверяет список ip-адресов

Допустим нам нужно проверить что запрос пришел с определенного ip-адреса (пример реальный из интеграции [Ю-кассы](https://yookassa.ru/developers/using-api/webhooks?ysclid=lv1ivds39j386472263#ip))
```python
def view(request):
    masks = (
        '185.71.76.0/27', '185.71.77.0/27', '77.75.153.0/25', '77.75.156.11',
        '77.75.156.35', '77.75.154.128/25', '2a02:5180::/32'
    )

    if not check_ip_match_the_masks(get_client_ip(request), masks):
        raise Http404()
```
Если кто-то, отсылает запрос с левого адреса получает 404 ошибку.