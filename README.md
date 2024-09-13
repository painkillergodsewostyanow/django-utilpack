# django-utilpack

### Сборник шаблонов и реализаций различных декораторов, утилит, фильтров, и других полезностей для django

* [access_decorator.py](decorators%2Faccess_decorator.py) - В django есть декоратор @login_required который перед выполнением обработчика, проверят авторизован ли пользователь, если нет, то редиректит его на страницу авторизации, данный же декоратор выполняет тот же функционал, но условие, и действие определяете вы сами.
* [ru_plur_morph.py](filters%2Fru_plur_morph.py) - Фильтр, который позволяет указать три окончания слова, и определяет нужное в зависимости от количества сущностей.
* [is_mobile.py](utils%2Fis_mobile.py) - Используя информацию из HTTP_USER_AGENT определяет устройство пользователя
* [get_client_ip.py](utils%2Fget_client_ip.py) - Используя информацию из request определяет ip-адрес клиента
* [check_ip.py](utils%2Fcheck_ip.py) - Методы проверяющие совпадение ip-адреса с масками
* [param_search.py](utils%2Fparam_search.py) - Поиск по параметрам```field1 == value1 and field2 in value2,value3 or field4 != value4..```