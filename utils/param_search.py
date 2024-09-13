import re
from django.db.models import Q


class ParamSearch:

    def __init__(self, available_name_match, available_operator):
        self.AVAILABLE_NAME_MATCH = available_name_match
        self.AVAILABLE_OPERATORS = available_operator

    def parse_condition(self, condition):
        field, operator, value, err = None, None, None, None

        if not any(oper in condition for oper in self.AVAILABLE_OPERATORS):
            return field, operator, value, f"Неверный оператор в условии: '{condition}'"

        if ' != ' in condition:
            field, value = condition.split(' != ')
            operator = 'ne'

        elif ' == ' in condition:
            field, value = condition.split(' == ')
            operator = 'eq'

        elif ' not in ' in condition:
            field, value = condition.split(' not in ')
            operator = 'not_in'

        elif ' in ' in condition:
            field, value = condition.split(' in ')
            operator = 'in'

        elif ' >= ' in condition:
            field, value = condition.split(' >= ')
            operator = 'gte'

        elif ' <= ' in condition:
            field, value = condition.split(' <= ')
            operator = 'lte'

        elif ' > ' in condition:
            field, value = condition.split(' > ')
            operator = 'gt'

        elif ' < ' in condition:
            field, value = condition.split(' < ')
            operator = 'lt'

        elif ' like ' in condition:
            field, value = condition.split(' like ')
            operator = 'icontains'

        try:
            result = (field.strip(), operator, value.strip(), err)
        except Exception:
            return field, operator, value, 'Синтаксическая ошибка: пропущен пробел'
        return result

    def parse_query(self, query):
        err_lst = []
        split_pattern = r'\s+(AND|OR)\s+'
        query_parts = re.split(split_pattern, query, flags=re.IGNORECASE)
        q_objects = Q()
        exclude_objects = Q()
        current_operator = None

        for part in query_parts:
            if part.upper() in ('AND', 'OR'):
                current_operator = part
            else:
                field, operator, value, err = self.parse_condition(part)

                if err:
                    err_lst.append(err)
                    continue

                q_object = self.create_q_object(field, operator, value)

                if isinstance(q_object, dict) and 'exclude' in q_object:
                    if current_operator and current_operator.upper() == 'OR':
                        exclude_objects |= q_object['exclude']
                    else:
                        exclude_objects &= q_object['exclude']
                elif q_object and not isinstance(q_object, (str,)):
                    if current_operator and current_operator.upper() == 'OR':
                        q_objects |= q_object
                    else:
                        q_objects &= q_object
                else:
                    err_lst.append(q_object)

        return q_objects, exclude_objects, err_lst

    def create_q_object(self, field, operator, value):
        field_m = self.match_field_name(field)
        if field_m:
            if operator not in ('eq', 'ne', 'in', 'not_in'):
                return Q(**{f"{field_m}__{operator}": value})

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

        return f"Поле {field} не найдено"

    def match_field_name(self, field):
        return self.AVAILABLE_NAME_MATCH.get(field, )
