import datetime
import time
import requests
from typing import Optional

from rest_framework.generics import get_object_or_404

from config import settings
from core.configs.api import MAILING_NUMBER_OF_ATTEMPTS, API_TOKEN
from apps.api.models.models import Message, UnsentMessage, Mailing
from apps.api import tasks

class SendMessageService:

    def send_messages(self, data: Optional[dict]) -> Optional[int]:
        """

        :param data:
        :return: Optional[int]
        """
        message_id = data.get('message_id')
        phone = data.get('phone')
        text = data.get('text')

        unsent = None
        message = get_object_or_404(Message, id=message_id)

        for i in range(MAILING_NUMBER_OF_ATTEMPTS):
            data = {
                'id': message_id,
                'phone': phone,
                'text': text
            }

            headers = {
                'accept': 'application/json',
                "Authorization": f'Bearer {API_TOKEN}',
                'Content-Type': 'application/json',
            }

            response = requests.post(
                url=f'https://probe.fbrq.cloud/v1/send/{message_id}',
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                message.status = True
                message.datetime_sending = datetime.datetime.now()
                message.save()
                return response.status_code
            else:
                if not unsent:
                    unsent = message.id

            time.sleep(15)
        return unsent


    def get_message_data(self, mailing_id: Optional[int]) -> list:
        """

        :param mailing_id:
        :return: list
        """
        data = []

        mailing = Mailing.objects.filter(id=mailing_id).first()

        if mailing:
            for client in mailing.client_filter.all():
                message = Message.objects.filter(client=client, mailing_id=mailing_id, status=False).first()

                if message:
                    row = {
                        'phone': client.phone,
                        'text': mailing.message_text,
                        'message_id': message.id,
                        'mailing_id': mailing.id
                    }
                else:
                    continue

                if client.timezone:
                    row['datetime_start'] = mailing.datetime_start.astimezone(client.timezone)
                    row['datetime_end'] = mailing.datetime_end.astimezone(client.timezone)

                else:
                    row['datetime_start'] = mailing.datetime_start.astimezone(settings.TIME_ZONE)
                    row['datetime_end'] = mailing.datetime_end.astimezone(settings.TIME_ZONE)
                data.append(row)
            return data

        else:
            raise Mailing.DoesNotExist('Рассылки с таким идентификатором не существует')

    def run_celery_task(self, mailing_id: Optional[int]) -> None:
        """

        :param mailing_id:
        """
        message_data = SendMessageService().get_message_data(mailing_id=mailing_id)
        for data in message_data:
            datetime_start = data.get('datetime_start')
            tasks.send_messages_task.apply_async(args=[data], eta=datetime_start)

    def get_unsent_messages(self) -> list:
        """

        :return: list
        """
        unsent_messages = UnsentMessage.objects.all()
        unsent_messages_list = []
        for message in unsent_messages:
            unsent_messages_list.append(message.id)

        return unsent_messages_list