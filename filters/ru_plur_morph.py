from django import template

register = template.Library()


@register.filter
def ru_plur_morph(count_entities, morph_vers):
    first_vrs, second_vrs, third_vrs = morph_vers.split(',')

    if count_entities == 1:
        return first_vrs
    if 5 > count_entities > 1:
        return second_vrs
    else:
        return third_vrs
