from django.db import models


class Question(models.Model):
    question_text = models.TextField(
        verbose_name="Текст ворпроса",
        db_index=True
    )
    answer = models.TextField(
        verbose_name="Ответ",
        db_index=True
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f"Вопрос {self.pk}"
