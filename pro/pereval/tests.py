from datetime import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from .serializers import PerevalAddedSerializer


class PerevalApiTEstCase(APITestCase):
    def setUp(self):
        # Объект - Перевал 1
        self.pereval_1 = PerevalAdded.objects.create(
            beauty_title='пер.',
            title='Кельт',
            other_titles='Вылов',
            connect='',
            status='new',
            user=Users.objects.create(
                email='kim@mail.ru',
                fam='Ким',
                name='Иван',
                otc='Сергеевич',
                phone="+7 321 53 78"
            ),
            coords=Coords.objects.create(
                latitude=54.6547,
                longitude=3.2164,
                height=2134,
            ),
            level=Level.objects.create(
                summer="1Б",
                autumn="2А",
                winter="1А",
                spring="1А"
            ),
        )

        # Объект - Перевал 2
        self.pereval_2 = PerevalAdded.objects.create(
            beauty_title='пер.',
            title='Дефолт',
            other_titles='Трумф',
            connect='',
            status='new',
            user=Users.objects.create(
                email='kim@mail.ru',
                fam='Ким',
                name='Иван',
                otc='Сергеевич',
                phone="+7 321 53 78"
            ),
            coords=Coords.objects.create(
                latitude=55.3545,
                longitude=11.3465,
                height=1100,
            ),
            level=Level.objects.create(
                summer="2Б",
                autumn="1А",
                winter="",
                spring=""
            ),
        )

    def test_get_perevals(self):
        url = reverse('submitData-list')
        response = self.client.get(url)
        serializer_data = PerevalAddedSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Проверяю корректность передаваемых данных
    def test_pereval_detail(self):
        url = reverse('submitData-detail', args=(self.pereval_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalAddedSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PerevalAddedSerializerApiTest(APITestCase):
    def setUp(self):
        # Объект - Перевал 1
        self.pereval_1 = PerevalAdded.objects.create(
            beauty_title='пер.',
            title='Кельт',
            other_titles='Вылов',
            connect='',
            status='new',
            user=Users.objects.create(
                email='kim@mail.ru',
                fam='Ким',
                name='Иван',
                otc='Сергеевич',
                phone="+7 321 53 78"
            ),
            coords=Coords.objects.create(
                latitude=54.6547,
                longitude=3.2164,
                height=2134,
            ),
            level=Level.objects.create(
                summer="1Б",
                autumn="2А",
                winter="1А",
                spring="1А"
            ),
        )

    def test_check(self):
        serializer_data = PerevalAddedSerializer(self.pereval_1).data
        expected_data = {
            "id": 1,
            "add_time": self.pereval_1.add_time.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "user": {
                "id": 1,
                "email": "kim@mail.ru",
                "fam": "Ким",
                "name": "Иван",
                "otc": "Сергеевич",
                "phone": "+7 321 53 78"
            },
            "coords": {
                "id": 1,
                "latitude": 54.6547,
                "longitude": 3.2164,
                "height": 2134
            },
            "level": {
                "id": 1,
                "summer": "1Б",
                "autumn": "2А",
                "winter": "1А",
                "spring": "1А"
            },
            "beauty_title": "пер.",
            "title": "Кельт",
            "other_titles": "Вылов",
            "connect": "",
            "status": "new"
        }
        self.assertEqual(serializer_data, expected_data)
