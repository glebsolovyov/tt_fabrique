from django.db import models

from timezone_utils.fields import TimeZoneField
from timezone_utils.choices import GROUPED_COMMON_TIMEZONES_CHOICES

from core.validators import validate_phone_number, validate_operator_code

from . import managers

class Mailing(models.Model):
    datetime_start = models.DateTimeField()
    message_text = models.TextField()
    client_filter = models.ManyToManyField('Client', related_name='clients')
    datetime_end = models.DateTimeField()

    objects = managers.MailingManager()


class Client(models.Model):
    phone = models.CharField(max_length=12, validators=[validate_phone_number])
    operator_code = models.CharField(max_length=3, validators=[validate_operator_code])
    tag = models.CharField(max_length=255)
    timezone = TimeZoneField(choices=GROUPED_COMMON_TIMEZONES_CHOICES, null=True)



class Message(models.Model):
    datetime_sending = models.DateTimeField()
    status = models.BooleanField(default=False)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ManyToManyField('Client', related_name='message_clients')


class UnsentMessage(models.Model):
    message = models.ForeignKey(Message, models.CASCADE)
