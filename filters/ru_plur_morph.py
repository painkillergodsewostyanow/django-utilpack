from django import template

register = template.Library()


@register.filter
def ru_plur_morph(count_entities, morph_vers):
    first_vrs, second_vrs, third_vrs = morph_vers.split(',')

    # Получаем последнюю цифру числа
    last_digit = count_entities % 10
    last_two_digits = count_entities % 100

    # Проверяем особые случаи для 11-14
    if 11 <= last_two_digits <= 14:
        return third_vrs

    # Определяем форму слова по последней цифре числа
    if last_digit == 1:
        return first_vrs
    elif 2 <= last_digit <= 4:
        return second_vrs
    else:
        return third_vrs
