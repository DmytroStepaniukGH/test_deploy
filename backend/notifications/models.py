from django.db import models


class Notification(models.Model):
    patient = models.ForeignKey(to='users.Patient', on_delete=models.CASCADE, related_name='notification')
    title = models.CharField(verbose_name='Заголовок сповіщення', max_length=100)
    text = models.CharField(verbose_name='Текст сповіщення', max_length=150)
    is_read = models.BooleanField(verbose_name='Прочитано: ', default=False)

    def __str__(self):
        return f'Сповіщення {self.patient}. {self.title}'