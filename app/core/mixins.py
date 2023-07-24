from typing import Optional

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT


class APIViewMixin(APIView):
    model = None
    serializer_class = None

    def get(self, request, pk):
        serializer = self.serializer_class(self.__validate_row(pk=pk))

        return Response(data=serializer.data)

    def put(self, request, pk):
        data = request.data
        serializer = self.serializer_class(self.__validate_row(pk=pk), data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)

        return Response(data=serializer.data, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.__validate_row(pk=pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def __validate_row(self, pk: Optional[int]):
        try:
            row = self.model.objects.filter(id=pk).first()
            return row
        except self.model.DoesNotExist:
            return Response(status=HTTP_400_BAD_REQUEST)



class CreateAPIViewMixin(APIView):
    serializer_class = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)