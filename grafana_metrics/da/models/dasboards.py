from django.db import models


class Dashboard(models.Model):
    title = models.TextField(verbose_name='Название', max_length=256)

    class Meta:
        db_table = 'dashboards'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title
