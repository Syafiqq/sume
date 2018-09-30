from django import template

register = template.Library()


@register.filter(name='is_same_menu')
def first_or_default(menu, comparator='', style='active'):
    return style if menu == comparator else ''
