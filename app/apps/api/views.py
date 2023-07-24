from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models.models import Mailing, Client, Message
from apps.api.serializers import MailingSerializer, ClientSerializer, MessageSerializer
from core.mixins import APIViewMixin, CreateAPIViewMixin
from core.services.client_service import ClientService
from core.services.mailing_service import MailingService
from core.services.send_messages_service import SendMessageService


class MailingAPIView(APIViewMixin):
    model = Mailing
    serializer_class = MailingSerializer


class MailingCreateAPIView(CreateAPIViewMixin):
    serializer_class = MailingSerializer


class MailingStatisticsAPIView(APIView):
    model = Mailing
    serializer_class = MailingSerializer

    def get(self, request):
        return Response(data=MailingService().get_statistics_for_mailings())


class MailingDetailedStatisticsAPIView(APIView):
    model = Mailing
    serializer_class = MailingSerializer

    def get(self, request):
        return Response(data=MailingService().get_detailed_statistics_for_mailings())


class ClientAPIView(APIViewMixin):
    model = Client
    serializer_class = ClientSerializer


class ClientCreateAPIView(CreateAPIViewMixin):
    serializer_class = ClientSerializer

    def post(self, request):
        data = request.data
        timezone = data.get('timezone')

        return ClientService().create(data=data, timezone=timezone)



class MessageAPIView(APIViewMixin):
    model = Message
    serializer_class = MessageSerializer


class MessageCreateAPIView(CreateAPIViewMixin):
    serializer_class = MessageSerializer


class SendMessageToClientAPIView(APIView):
    model = Message
    serializer_class = MessageSerializer

    def get(self, request, pk):
        unsent_messages = SendMessageService().get_unsent_messages()
        try:
            SendMessageService().run_celery_task(mailing_id=pk)
            return Response(data={'unsent_messages': unsent_messages})
        except (Mailing.DoesNotExist, ConnectionError) as error:
            Response(data={'error': error})
