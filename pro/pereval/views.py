from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import *
import django_filters


# Базовый класс для ViewSet'ов
class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.model.objects.all()


# ViewSet для модели Users
class UsersViewset(BaseViewSet):
    serializer_class = UsersSerializer
    model = Users
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['fam', 'name', 'otc', 'email']

    def create(self, request, *args, **kwargs):
        # Создание объекта пользователя
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Успех!',
                    'id': serializer.data['email'],
                }
            )
        # Обработка ошибок валидации и внутренней ошибки сервера
        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Некорректный запрос.',
                    'id': None,
                }
            )
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка при выполнении операции.',
                    'id': None,
                }
            )


# ViewSet для модели PerevalAdded
class PerevalViewSet(BaseViewSet):
    serializer_class = PerevalAddedSerializer
    model = PerevalAdded

    def create(self, request, *args, **kwargs):
        # Создание объекта PerevalAdded
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': None,
                'id': serializer.data['id'],
            })
        # Обработка ошибок валидации и внутренней ошибки сервера
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'id': None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Ошибка подключения к базе данных.',
                'id': None,
            })

    def partial_update(self, request, *args, **kwargs):
        # Частичное обновление объекта PerevalAdded
        perevals = self.get_object()
        if perevals.status == 'new':
            serializer = PerevalAddedSerializer(perevals, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'message': 'Запись успешно изменена.'
                })
            else:
                return Response({
                    'state': '0',
                    'message': serializer.errors
                })
        else:
            return Response({
                'state': '0',
                'message': f"Не удалось обновить сведения, так как запись уже у модератора. "
                           f"Статус: {perevals.get_status_display()}."
            })


# APIView для получения списка объектов PerevalAdded, которые добавил пользователь с email
class EmailAPIView(generics.ListAPIView):
    serializer_class = PerevalAddedSerializer

    def get_queryset(self):
        email = self.request.query_params.get('user__email', None)
        user_instance = get_object_or_404(Users, email=email)
        return PerevalAdded.objects.filter(user=user_instance)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
