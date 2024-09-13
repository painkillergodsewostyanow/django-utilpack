import re
from django.db.models import Q


class ParamSearch:

    OPERATORS_MAP = {
        ' != ': 'ne',
        ' == ': 'eq',
        ' not in ': 'not_in',
        ' in ': 'in',
        ' >= ': 'gte',
        ' <= ': 'lte',
        ' > ': 'gt',
        ' < ': 'lt',
        ' like ': 'icontains'
    }

    def __init__(self, available_name_match: dict, available_operator: list):
        self.AVAILABLE_NAME_MATCH = available_name_match
        self.AVAILABLE_OPERATORS = available_operator

    def __parse_condition(self, condition: str) -> tuple:
        """Разбирает условие и возвращает кортеж (поле, оператор, значение, ошибка)"""
        if not any(oper in condition for oper in self.OPERATORS_MAP):
            return None, None, None, f"Неверный оператор в условии: '{condition}'"

        for oper, orm_oper in self.OPERATORS_MAP.items():
            if oper in condition:
                try:
                    field, value = condition.split(oper)
                    return field.strip(), orm_oper, value.strip(), None
                except ValueError:
                    return None, None, None, "Синтаксическая ошибка: неверный формат условия"

        return None, None, None, "Не удалось распознать условие"

    def parse_query(self, query: str) -> tuple:
        """Парсит строку запроса в объект Q"""
        err_lst = []
        split_pattern = r'\s+(AND|OR)\s+'
        query_parts = re.split(split_pattern, query, flags=re.IGNORECASE)
        q_objects = Q()
        exclude_objects = Q()
        current_operator = None

        for part in query_parts:
            if part.upper() in ('AND', 'OR'):
                current_operator = part.upper()
            else:
                field, operator, value, err = self.__parse_condition(part)

                if err:
                    err_lst.append(err)
                    continue

                q_object = self.__create_q_object(field, operator, value, err_lst)

                if q_object is None:
                    continue

                if isinstance(q_object, dict) and 'exclude' in q_object:
                    if current_operator == 'OR':
                        exclude_objects |= q_object['exclude']
                    else:
                        exclude_objects &= q_object['exclude']
                else:
                    if current_operator == 'OR':
                        q_objects |= q_object
                    else:
                        q_objects &= q_object

        return q_objects, exclude_objects, err_lst

    def __create_q_object(self, field: str, operator: str, value: str, err_lst: list):
        """Создает объект Q на основе поля, оператора и значения"""
        field_m = self.__match_field_name(field)

        if not field_m:
            err_lst.append(f"Поле {field} не найдено")
            return None

        if operator in ('eq', 'ne', 'in', 'not_in'):
            if operator == 'eq':
                return Q(**{field_m: value})
            elif operator == 'ne':
                return {'exclude': Q(**{field_m: value})}
            elif operator == 'in':
                value_list = value.split(',')
                return Q(**{f"{field_m}__in": value_list})
            elif operator == 'not_in':
                value_list = value.split(',')
                return {'exclude': Q(**{f"{field_m}__in": value_list})}
        else:
            return Q(**{f"{field_m}__{operator}": value})

    def __match_field_name(self, field: str) -> str:
        """Возвращает правильное имя поля или None, если поле не найдено"""
        return self.AVAILABLE_NAME_MATCH.get(field)

