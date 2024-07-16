from django import template
import math

register = template.Library()


@register.filter(name='reading_time')
def reading_time_filter(content, wpm=200):
    words = len(content.split())
    reading_time_min = math.ceil(words / wpm)
    return reading_time_min
