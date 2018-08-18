from django import template

register = template.Library()


@register.filter(name='first_or_default')
def first_or_default(array, default=''):
    from app.app.utils.arrayutil import first_or_default as fod
    return fod(array, default)
