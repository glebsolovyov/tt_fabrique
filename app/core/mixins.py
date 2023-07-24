from typing import Optional

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT


class APIViewMixin(APIView):
    model = None
    serializer_class = None

    def get(self, request, pk: Optional[int]) -> Response:
        """

        :param request:
        :param pk:
        :return: Response
        """
        row = self.__validate_row(pk=pk)

        if row:
            serializer = self.serializer_class(row)
            return Response(data=serializer.data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk: Optional[int]) -> Response:
        """

        :param request:
        :param pk:
        :return: Response
        """
        row = self.__validate_row(pk=pk)
        data = request.data

        if row:
            serializer = self.serializer_class(row, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: Optional[int]) -> Response:
        """

        :param request:
        :param pk:
        :return: Response
        """
        row =  self.__validate_row(pk=pk)

        if row:
            row.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(status=HTTP_400_BAD_REQUEST)


    def __validate_row(self, pk: Optional[int]):
        """

        :param pk:
        :return:
        """
        row = self.model.objects.filter(id=pk).first()

        if row:
            return row

        return None



class CreateAPIViewMixin(APIView):
    serializer_class = None

    def post(self, request) -> Response:
        """

        :param request:
        :return: Response
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)