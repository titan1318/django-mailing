from datetime import datetime

from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.filter
def clients_word_form(count):
    if count % 10 == 1 and count % 100 != 11:
        return "клиент"
    elif count % 10 in [2, 3, 4] and not (count % 100 in [12, 13, 14]):
        return "клиента"
    else:
        return "клиентов"


@register.filter
def users_word_form(count):
    if count % 10 == 1 and count % 100 != 11:
        return "пользователь"
    elif count % 10 in [2, 3, 4] and not (count % 100 in [12, 13, 14]):
        return "пользователя"
    else:
        return "пользователей"


@register.filter
def mailings_word_form(count):
    if count % 10 == 1 and count % 100 != 11:
        return "рассылка"
    elif count % 10 in [2, 3, 4] and not (count % 100 in [12, 13, 14]):
        return "рассылки"
    else:
        return "рассылок"
