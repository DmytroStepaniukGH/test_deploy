from django.db import models


class PatientCard(models.Model):
    card_id = models.AutoField(verbose_name='Картка №', primary_key=True, unique=True)
    patient = models.OneToOneField(to='users.Patient', on_delete=models.CASCADE, related_name='card')
    register_date = models.DateField(verbose_name='Дата реєстрації', editable=False, auto_now_add=True)
    blood_group = models.CharField(verbose_name='Група крові', max_length=20)
    traumas_info = models.CharField(verbose_name='Травми', max_length=5000)
    operations_info = models.CharField(verbose_name='Операції', max_length=5000)
    chronical_illness_info = models.CharField(verbose_name='Хронічні захворювання', max_length=5000)

    def __str__(self):
        return f'Картка № {self.card_id}. {self.patient}'
