from django import template
register = template.Library()


@register.filter
def list_index(current_top_num,  forloop):
    return (current_top_num - forloop)