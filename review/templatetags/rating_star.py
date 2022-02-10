from django import template

register = template.Library()


@register.filter
def rating_star(rating):
    return rating * '★' + (5 - rating) * '☆'
