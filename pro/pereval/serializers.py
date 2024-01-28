from rest_framework import serializers
from .models import *


# Сериализатор для модели Users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


# Сериализатор для модели Coords
class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


# Сериализатор для модели Level
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


# Сериализатор для модели PerevalImages
class PerevalImagesSerializer(serializers.ModelSerializer):
    # Форматирование даты и времени при сериализации
    date_added = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = PerevalImages
        exclude = ('date_added',)  # исключение поля date_added из сериализации


# Сериализатор для модели PerevalAreas
class PerevalAreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAreas
        fields = '__all__'


# Сериализатор для модели SprActivitiesTypes
class SprActivitiesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprActivitiesTypes
        fields = '__all__'


# Сериализатор для модели PerevalAdded
class PerevalAddedSerializer(serializers.ModelSerializer):
    # Форматирование даты и времени при сериализации
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    # Вложенные сериализаторы для связанных моделей
    user = UsersSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    # Метод для создания нового объекта
    def create(self, validated_data):
        # Получение или создание пользователя
        user, _ = Users.objects.get_or_create(**validated_data.pop('user'))

        # Создание координат и уровня сложности
        coords = Coords.objects.create(**validated_data.pop('coords'))
        level = Level.objects.create(**validated_data.pop('level'))

        # Создание объекта PerevalAdded
        pereval = PerevalAdded.objects.create(**validated_data, user=user, coords=coords, status='new', level=level)

        return pereval

    def update(self, instance, validated_data):
        # Обновление полей сущности PerevalAdded
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.add_time = validated_data.get('add_time', instance.add_time)
        instance.status = validated_data.get('status', instance.status)

        # Обновление связанных полей level
        level_data = validated_data.get('level', {})
        instance.level.summer = level_data.get('summer', instance.level.summer)
        instance.level.autumn = level_data.get('autumn', instance.level.autumn)
        instance.level.winter = level_data.get('winter', instance.level.winter)
        instance.level.spring = level_data.get('spring', instance.level.spring)
        instance.level.save()

        # Обновление связанных полей coords
        coords_data = validated_data.get('coords', {})
        instance.coords.latitude = coords_data.get('latitude', instance.coords.latitude)
        instance.coords.longitude = coords_data.get('longitude', instance.coords.longitude)
        instance.coords.height = coords_data.get('height', instance.coords.height)
        instance.coords.save()

        # Пользователя беру существующего
        user_data = validated_data.get('user', {})
        user = Users.objects.get(**user_data)
        instance.user = user

        instance.save()
        return instance

    # Валидация данных перед сохранением
    def validate(self, data):
        # Если объект уже существует, даю понять, что данные пользователя изменить нельзя
        if self.instance and any(data['user'][field] != getattr(self.instance.user, field) for field in
                                 ['email', 'fam', 'name', 'otc', 'phone']):
            raise serializers.ValidationError({'Данные пользователя не могут быть изменены.'})
        return data
