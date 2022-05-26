from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name="Имя на английском",
        blank=True,
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name="Имя на японском",
        blank=True,
    )
    image = models.ImageField(
        upload_to='images',
        verbose_name="Ссылка на изображение",
    )
    description = models.TextField(
        blank=True
    )
    evolution = models.ForeignKey(
        'self',
        verbose_name="Из кого эволюционировал",
        blank=True,
        null=True,
        related_name='next_evolutions',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(
        Pokemon,
        verbose_name="Ссылка на покемона",
        on_delete=models.CASCADE,
    )
    lat = models.FloatField(
        max_length=200,
        verbose_name="Широта",
    )
    lon = models.FloatField(
        max_length=200,
        verbose_name="Долгота",
    )
    appeared_at = models.DateTimeField(
        default=None,
        verbose_name="Время появления",
    )
    disappeared_at = models.DateTimeField(
        default=None,
        verbose_name="Время исчезновения",
    )
    level = models.IntegerField(
        default=0,
        blank=True,
        verbose_name="Уровень",
    )
    health = models.IntegerField(
        default=0,
        blank=True,
        verbose_name="Здоровье",
    )
    strength = models.IntegerField(
        default=0,
        blank=True,
        verbose_name="Сила",
    )
    defence = models.IntegerField(
        default=0,
        blank=True,
        verbose_name="Защита",
    )
    stamina = models.IntegerField(
        default=0,
        blank=True,
        verbose_name="Выносливость",
    )

    def __str__(self):
        return f'{self.Pokemon.title} {self.level} уровень'

