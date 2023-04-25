from django.db import models


RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Review(models.Model):
    appointment = models.OneToOneField(to='users.Appointment', on_delete=models.CASCADE, default=1)
    doctor = models.ForeignKey(to='users.Doctor', on_delete=models.CASCADE, default=1)
    review_rating = models.IntegerField(verbose_name='Оцінка', default=5, choices=RATING_CHOICES)
    review_text = models.CharField(verbose_name='Відгук', max_length=2000)
    created_at = models.DateTimeField(verbose_name='Дата створення', auto_now_add=True)
