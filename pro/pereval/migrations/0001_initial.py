# Generated by Django 5.0.1 on 2024-01-26 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(max_length=20, verbose_name='Широта')),
                ('longitude', models.FloatField(max_length=20, verbose_name='Долгота')),
                ('height', models.IntegerField(verbose_name='Высота')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summer', models.CharField(blank=True, max_length=2, null=True, verbose_name='Лето')),
                ('autumn', models.CharField(blank=True, max_length=2, null=True, verbose_name='Осень')),
                ('winter', models.CharField(blank=True, max_length=2, null=True, verbose_name='Зима')),
                ('spring', models.CharField(blank=True, max_length=2, null=True, verbose_name='Весна')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('img', models.BinaryField()),
                ('title', models.CharField(max_length=128, verbose_name='Название картинки')),
            ],
        ),
        migrations.CreateModel(
            name='SprActivitiesTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('foot', 'Пешком'), ('ski', 'Лыжи'), ('catamaran', 'Катамаран'), ('kayak', 'Байдарка'), ('raft', 'Плот'), ('alloy', 'Сплав'), ('bicycle', 'Велосипед'), ('car', 'Автомобиль'), ('sail', 'Парус'), ('horseback', 'Верхом')], max_length=10, verbose_name='Тип похода')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('fam', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('otc', models.CharField(max_length=50, verbose_name='Отчество')),
                ('phone', models.TextField(verbose_name='Телефон')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(max_length=128, verbose_name='Топоним')),
                ('title', models.CharField(max_length=128, verbose_name='Название перевала')),
                ('other_titles', models.CharField(max_length=128, verbose_name='Дополнительное название')),
                ('connect', models.CharField(blank=True, max_length=128, null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('status', models.CharField(choices=[('new', 'Создано'), ('pending', 'Взято в работу'), ('accepted', 'Принято'), ('rejected', 'Отклонено')], default='new', max_length=10)),
                ('coords', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pereval.coords')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.level')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pereval.users')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalAreas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название зоны')),
                ('id_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.perevaladded')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalAddedImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pereval_added', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.perevaladded')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.perevalimages')),
            ],
        ),
    ]
