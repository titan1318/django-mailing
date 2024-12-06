from django.db import models

NULLABLE = {'blank': True, 'null': False}


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Статья')
    preview = models.ImageField(upload_to="blog/post_preview", verbose_name="Превью", **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    number_of_views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=False, verbose_name="Добавить к избранным")

    def __str__(self):
        return f'{self.title} от {self.created_at} ({self.is_published})'




    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
