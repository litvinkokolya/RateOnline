from django.db import models
from django.urls import reverse


class User(models.Model):

    first_name = models.CharField(max_length=100,
                            help_text="Введите имя участника",
                            verbose_name="Имя участника")

    last_name = models.CharField(max_length=100,
                            help_text="Введите фамилию участника",
                            verbose_name="Фамилия участника")

    # image = models.ImageField(upload_to='images/')

    phone_number = models.CharField(max_length=11,
                                   help_text="Введите номер участника",
                                   verbose_name="Номер участника")

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    nom = models.ManyToManyField('Nominations', verbose_name='Номинации')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return self.last_name


class Referee(models.Model):

    first_name = models.CharField(max_length=100,
                            help_text="Введите имя судьи",
                            verbose_name="Имя судьи")

    last_name = models.CharField(max_length=100,
                            help_text="Введите фамилию судьи",
                            verbose_name="Фамилия судьи")

    # image = models.ImageField(upload_to='images/')

    phone_number = models.CharField(max_length=11,
                                   help_text="Введите номер судьи",
                                   verbose_name="Номер судьи")

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    nom = models.ManyToManyField('Nominations', verbose_name='Номинации')

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'

    def __str__(self):
        return self.last_name


class Category(models.Model):

    name = models.CharField(max_length=10,
                                    help_text="Введите название категории",
                                    verbose_name="Название категории")

    description = models.TextField(max_length=100,
                                    help_text="Введите описание категории",
                                    verbose_name="Описание категории")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Nominations(models.Model):

    name = models.CharField(max_length=50,
                                    help_text="Введите название номинации",
                                    verbose_name="Название номинации")

    cat = models.ManyToManyField('Category', verbose_name='Категория')

    class Meta:
        verbose_name = 'Номинация'
        verbose_name_plural = 'Номинации'
        ordering = ['id']

    def __str__(self):
        return self.name


class Atribute(models.Model):

    name = models.CharField(max_length=50,
                                    help_text="Введите название атрибута",
                                    verbose_name="Название атрибута")

    nom = models.ForeignKey('Nominations', on_delete=models.PROTECT, verbose_name='Номинация')

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return self.name


class Work(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='Участник')

    nom = models.ForeignKey('Nominations', on_delete=models.PROTECT, verbose_name='Номинация')

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self) -> str:
        return f"Участник: {self.user} в номинации {self.nom}"


class Score(models.Model):
    value = models.IntegerField(help_text="Введите оценку", verbose_name="Оценка")

    ref = models.ForeignKey('Referee', on_delete=models.PROTECT, verbose_name='Судья')

    work = models.ForeignKey('Work', on_delete=models.PROTECT, verbose_name='Работа')

    atrib = models.ForeignKey('Atribute', on_delete=models.PROTECT, verbose_name='Атрибут')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self) -> str:
        return f"Работа: {self.work} в атрибуте {self.atrib}"
