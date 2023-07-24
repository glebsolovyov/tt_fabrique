from typing import Optional

from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from apps.api.models.models import Client
from apps.api.serializers import ClientSerializer


class ClientService:

    model = Client

    def create(self, data: Optional[dict], timezone: Optional[str]):
        new_data = data.copy()

        if not timezone:
            new_data['timezone'] = 'Europe/Moscow'

        serializer = ClientSerializer(data=new_data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        return Response(data=serializer.data, status=HTTP_400_BAD_REQUEST)