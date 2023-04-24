from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager # noqa


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField(verbose_name='Імʼя', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='Прізвище', max_length=150, blank=True)
    patronim_name = models.CharField(verbose_name='По-батькові', max_length=150, blank=True)
    birth_date = models.CharField(verbose_name='Дата народження', max_length=10, blank=True)
    email = models.EmailField(verbose_name='Email', unique=True, blank=True)
    phone_num = models.CharField(verbose_name='Номер телефону', max_length=13, blank=True)
    sex = models.CharField(verbose_name='Стать', max_length=10, blank=True)
    address_city = models.CharField(verbose_name='Місто', max_length=50, blank=True)
    address_street = models.CharField(verbose_name='Вулиця', max_length=150, blank=True)
    address_house = models.CharField(verbose_name='Будинок', max_length=10, blank=True)
    address_appartment = models.CharField(verbose_name='Квартира', max_length=10, blank=True)
    is_confirmed = models.BooleanField(verbose_name='Верифікований', default=0, blank=True)
    is_doctor = models.BooleanField(verbose_name='Чи є лікарем', default=0, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        db_table = 'accounts'

    def save(self, *args, **kwargs):
        need_to_create_patient = False

        if not self.id:
            need_to_create_patient = True
        super().save(*args, **kwargs)

        if need_to_create_patient:
            apps.get_model(*'users.Patient'.split('.')).objects.create(user=self)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.last_name} {self.first_name} {self.patronim_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_full_address(self):
        return f'{self.address_city}, {self.address_street} ' \
               f'{self.address_house}, {self.address_appartment}'