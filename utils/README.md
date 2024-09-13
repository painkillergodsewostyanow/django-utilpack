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

[param_search.py](param_search.py) - Поиск по параметрам (field1 == value1 and field2 in value2,value3 or field4 != value4..)

```python
from param_search import ParamSearch
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание категории")


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")


    
AVAILABLE_NAME_MATCH = {
    # Поле для поиска: название поля в БД/ORM
    'name': 'name',
    'n': 'name',
    'price': 'price',
    'p': 'price',
    'category': 'category__name', # django lookup
    'c': 'category__name',
    'category_description': 'category__description',
    'cd': 'category__description',
}

AVAILABLE_OPERATORS = ('!=', '==', 'not in', 'in', '>', '<', '>=', '<=', 'like')

def search(search_query, query):
    qs = ParamSearch(AVAILABLE_NAME_MATCH, AVAILABLE_OPERATORS)
    q_, q_ex, err = qs.parse_query(search_query)
    try:
        query = query.filter(q_).exclude(q_ex)
    except ValueError as e:
        err.append(e)

    return query, err


queryset = Product.objects.all()
search_param = 'category == Молочная продукция and price <= 100'

search(search_param, queryset)


```