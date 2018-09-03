import json

from django import template

register = template.Library()


@register.filter(name='dump_json_dict')
def dump_json_dict(data):
    if not isinstance(data, dict):
        return json.dumps({})
    return json.dumps(data)


@register.filter(name='dump_json_array')
def dump_json_array(data):
    if not isinstance(data, list):
        return json.dumps([])
    return json.dumps(data)
