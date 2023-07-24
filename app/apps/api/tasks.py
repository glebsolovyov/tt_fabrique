import datetime
from typing import Optional
import pytz

from django.http import Http404

from apps.api.models.models import Mailing, UnsentMessage
from requests.exceptions import ConnectionError
from config.celery import app

from core.services import send_messages_service


@app.task
def send_messages_task(data: Optional[dict]) -> dict:
    """

    :param data:
    :return: dict
    """
    try:
        datetime_now = datetime.datetime.now().astimezone(pytz.timezone('Europe/Moscow'))
        datetime_end = data.get('datetime_end')

        if datetime_now < datetime_end:
            result = send_messages_service.SendMessageService().send_messages(data)
            print(result)
            if result != 200:
                UnsentMessage.objects.create(message_id=result)

    except (Mailing.DoesNotExist, ConnectionError, Http404) as error:
        return {'Error': error}



