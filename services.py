from django.core.cache import cache

from config.settings import CACHE_ENABLED


def get_data_from_cache(model):
    """ Получение данных модели из кэша, если кэс пуст получение с БД и добавление в кэш"""
    if not CACHE_ENABLED:
        return model.objects.all()

    key = f'{model._meta}_list'
    # print(key)
    models = cache.get(key)

    if models is not None:
        return models

    models = model.objects.all()
    cache.set(key, models)
    return models
