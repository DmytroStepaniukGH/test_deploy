from django.db import models


class StatusChoices(models.TextChoices):
    UNCONFIRMED = "Непідтверджений", "Непідтверджений"
    ACTIVE = "Активний", "Активний"
    COMPLETED = "Завершений", "Завершений"
