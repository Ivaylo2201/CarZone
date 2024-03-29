from django import template

import re

register = template.Library()


@register.filter
def separate_thousands(value: int) -> str:
    return "{:,}".format(value).replace(',', ' ')


@register.filter
def separate_digits(value: str) -> str:
    return f'+359 {" ".join(re.findall("...", value[1:]))}'
