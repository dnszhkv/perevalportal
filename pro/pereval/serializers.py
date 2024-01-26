from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class PerevalImagesSerializer(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = PerevalImages
        exclude = ('date_added',)  # исключаю поле date_added из сериализации


class PerevalAreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAreas
        fields = '__all__'


class SprActivitiesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprActivitiesTypes
        fields = '__all__'


class PerevalAddedSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = UsersSerializer()
    coords = CoordsSerializer()
    status = serializers.CharField(read_only=True)
    level = LevelSerializer()

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        user, created = Users.objects.get_or_create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        pereval = PerevalAdded.objects.create(**validated_data, user=user, coords=coords, status='new', level=level)

        return pereval

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.email != data_user['email'],
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Данные пользователя не могут быть изменены.'})
        return data
