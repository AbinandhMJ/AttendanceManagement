from django import template
import datetime

register = template.Library()

@register.filter
def format_duration(value):
    if not value:
        return 'nil'
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    if hours and minutes:
        return f'{hours} hrs {minutes} mins'
    elif hours:
        return f'{hours} hr' if hours == 1 else f'{hours} hrs'
    elif minutes:
        return f'{minutes} min' if minutes == 1 else f'{minutes} mins'
    else:
        return 'nil'
