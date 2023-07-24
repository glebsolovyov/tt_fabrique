from apps.api.models.models import Mailing, Message, Client
from apps.api.serializers import MailingSerializer


class MailingService:
    model = Mailing

    def __get_all_mailings(self):
        return self.model.objects.all()

    def get_statistics_for_mailings(self) -> list:
        """

        :return: list
        """
        data = []
        mailings = self.__get_all_mailings()
        for mailing in mailings:
            row = {
                'mailing': {
                    'id': mailing.id,
                    'datetime_start': mailing.datetime_start,
                    'message_text': mailing.message_text,
                    'datetime_end': mailing.datetime_end
                },
                'messages': {
                    'sent': Message.objects.filter(mailing_id=mailing.id, status=True).count(),
                    'not_sent': Message.objects.filter(mailing_id=mailing.id, status=False).count()
                }
            }

            data.append(row)

        return data

    def get_detailed_statistics_for_mailings(self) -> list:
        """

        :return: list
        """
        data = []
        mailings = self.__get_all_mailings()

        for mailing in mailings:
            clients = mailing.client_filter.all()
            row = {
                'mailing': {
                    'id': mailing.id,
                    'datetime_start': mailing.datetime_start,
                    'message_text': mailing.message_text,
                    'datetime_end': mailing.datetime_end
                },
                'messages': Message.objects.filter(mailing_id=mailing.id).values(),
                'clients': []
            }
            for client in clients:
                client_row = {
                    'id': client.id,
                    'phone': client.phone,
                    'operator_code': client.operator_code,
                    'tag': client.tag,
                    'timezone': str(client.timezone)
                }

                if row.get('clients'):
                    row['clients'].append(client_row)
                else:
                    row['clients'] = [client_row]

            data.append(row)

        return data
