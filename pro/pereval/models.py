from django.db import models


class Users(models.Model):
    email = models.EmailField()
    fam = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    otc = models.CharField(max_length=50, verbose_name='Отчество')
    phone = models.TextField(verbose_name='Телефон')


class Coords(models.Model):
    latitude = models.FloatField(max_length=20, verbose_name='Широта')
    longitude = models.FloatField(max_length=20, verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')


class PerevalImages(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    img = models.BinaryField()
    title = models.CharField(max_length=128, verbose_name='Название картинки')


class Level(models.Model):
    summer = models.CharField(max_length=2, null=True, blank=True, verbose_name='Лето')
    autumn = models.CharField(max_length=2, null=True, blank=True, verbose_name='Осень')
    winter = models.CharField(max_length=2, null=True, blank=True, verbose_name='Зима')
    spring = models.CharField(max_length=2, null=True, blank=True, verbose_name='Весна')


class PerevalAdded(models.Model):

    STATUS = [
        ('new', 'Создано'),
        ('pending', 'Взято в работу'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено')
    ]

    beauty_title = models.CharField(max_length=128, verbose_name='Топоним')
    title = models.CharField(max_length=128, verbose_name='Название перевала')
    other_titles = models.CharField(max_length=128, verbose_name='Дополнительное название')
    connect = models.CharField(max_length=128, null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.CharField(max_length=10, choices=STATUS, default='new')
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)
    coords = models.OneToOneField('Coords', on_delete=models.CASCADE)


class PerevalAddedImages(models.Model):
    pereval_added = models.ForeignKey('PerevalAdded', on_delete=models.CASCADE)
    image = models.ForeignKey('PerevalImages', on_delete=models.CASCADE)


class PerevalAreas(models.Model):
    id_parent = models.ForeignKey('PerevalAdded', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='Название зоны')


class SprActivitiesTypes(models.Model):

    TYPE = [
        ('foot', 'Пешком'),
        ('ski', 'Лыжи'),
        ('catamaran', 'Катамаран'),
        ('kayak', 'Байдарка'),
        ('raft', 'Плот'),
        ('alloy', 'Сплав'),
        ('bicycle', 'Велосипед'),
        ('car', 'Автомобиль'),
        ('sail', 'Парус'),
        ('horseback', 'Верхом'),
    ]

    title = models.CharField(max_length=10, choices=TYPE, verbose_name='Тип похода')
