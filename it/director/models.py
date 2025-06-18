from django.db import models

class TaskTemplate(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название шаблона")
    description = models.TextField(verbose_name="Описание")
    max_assigned_users = models.PositiveIntegerField(default=1, verbose_name="Максимальное количество исполнителей")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Шаблон задачи"
        verbose_name_plural = "Шаблоны задач"
