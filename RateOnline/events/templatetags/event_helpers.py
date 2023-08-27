from django import template

register = template.Library()


@register.simple_tag(name='get_score')
def get_score(scores, attribute_name, value):
    return 'checked disabled' if scores[attribute_name][0] == str(value) else 'disabled'
