from datetime import datetime
from django.db import models

from accounts.models import User

from users.choises import StatusChoices


TIME_CHOICES = (
    ("09:00", "09:00"),
    ("09:30", "09:30"),
    ("10:00", "10:00"),
    ("10:30", "10:30"),
    ("11:00", "11:00"),
    ("11:30", "11:30"),
    ("12:00", "12:00"),
    ("12:30", "12:30"),
    ("13:00", "13:00"),
    ("13:30", "13:30"),
    ("14:00", "14:00"),
    ("14:30", "14:30"),
    ("15:00", "15:00"),
    ("15:30", "15:30"),
    ("16:00", "16:00"),
    ("16:30", "16:30"),
    ("17:00", "17:00"),
    ("17:30", "17:30"),
)

SPECIALIZATION_CHOICES = (
    ("Дерматолог", "Дерматолог"),
    ("Кардіолог", "Кардіолог"),
    ("Пульмонолог", "Пульмонолог"),
    ("Невролог", "Невролог"),
    ("Терапевт", "Терапевт"),
    ("Гастроентеролог", "Гастроентеролог"),
)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.get_full_name()}'

    def create_appointment(self, doctor, date, time):
        appointment = Appointment(patient=self, doctor=doctor, date=date, time=time)
        appointment.save()


class Specialization(models.Model):
    name = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES,
                            default="Не обрано")
    image = models.FileField(verbose_name='Зображення спеціальності',
                             upload_to='specialization_images',
                             default='Cardiologist.svg')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(verbose_name='Фото профіля',
                                      upload_to='doctor_profile_photo',
                                      default="doctor_profile_photo/default_image.png",
                                      blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.RESTRICT,
                                       related_name='specialization')
    price = models.IntegerField(verbose_name='Вартість прийому')
    experience = models.CharField(verbose_name='Стаж', max_length=20)
    category = models.CharField(verbose_name='Категорія', max_length=30)
    info = models.CharField(verbose_name='Загальна нформація про лікаря',
                            max_length=1000, blank=True)
    education = models.CharField(verbose_name='Освіта', default='', max_length=1000)
    courses = models.CharField(verbose_name='Курси', default='', max_length=1000, blank=True)
    procedures_performed = models.CharField(verbose_name='Виконувані процедури', default='',
                                            max_length=1000, blank=True)

    def get_available_slots(self, date):
        time_dict = {}
        today = datetime.today().strftime('%Y-%m-%d')
        date = date.strftime('%Y-%m-%d')

        if date > today:
            for time_choice in TIME_CHOICES:
                time_dict[time_choice[0]] = True

        elif date == today:
            for time_choice in TIME_CHOICES:
                if not datetime.now().strftime('%H:%M') > time_choice[0]:
                    time_dict[time_choice[0]] = True
                else:
                    time_dict[time_choice[0]] = False
        else:
            for time_choice in TIME_CHOICES:
                time_dict[time_choice[0]] = False

            return {'date': date, 'doctor_id': self.id, 'time': time_dict}

        slots = {'date': date, 'doctor_id': self.id, 'time': time_dict}

        all_appointments = self.appointments.filter(date=date)
        unavailable_times = self.unavailable_time.filter(date=date).values_list('time', flat=True)

        for appointment in all_appointments:
            if appointment.time in slots['time'].keys():
                slots['time'][appointment.time] = False

        for time in slots['time'].keys():
            if time in unavailable_times:
                slots['time'][time] = False

        return slots

    def set_unavailable_time(self, date, time):
        unavailable_time = DoctorUnavailableTime(doctor=self, date=date, time=time)
        unavailable_time.save()

    def __str__(self):
        return f'{self.user.get_full_name()} / {self.specialization}' \
               f' / Email: {self.user.email} '


class DoctorUnavailableTime(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='unavailable_time')
    date = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES,
                            default="09:00")


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="09:00")
    status = models.CharField(max_length=15, choices=StatusChoices.choices,
                              default=StatusChoices.UNCONFIRMED)

    medical_history = models.CharField(verbose_name='Анамнез захворювання',
                                       default='', blank=True, max_length=1000)
    objective_status = models.CharField(verbose_name="Об'єктивний статус",
                                        default='', blank=True, max_length=1000)
    diagnosis = models.CharField(verbose_name='Діагноз',
                                 default='', blank=True, max_length=500)
    examination = models.CharField(verbose_name='Обстеження',
                                   default='', blank=True, max_length=1000)
    recommendations = models.CharField(verbose_name='Рекомендації',
                                       default='', blank=True, max_length=1000)

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f'{self.patient} запис до {self.doctor} {self.date} о {self.time}'


def check_date_time(date, time):
    today = datetime.today().strftime('%Y-%m-%d')
    time_now = datetime.now().strftime('%H:%M')

    if date > today:
        if time in (time, time) in TIME_CHOICES:
            return True
        else:
            return False

    elif date == today:
        if time >= time_now and (time, time) in TIME_CHOICES:
            return True
        else:
            return False

    else:
        return False
