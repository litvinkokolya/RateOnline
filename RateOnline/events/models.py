from django.db import models
from django.db.models import constraints

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


class Nomination(models.Model):
    name = models.CharField(max_length=50,
                            help_text="Введите название номинации",
                            verbose_name="Название номинации")

    photos_conf = models.JSONField(default=dict)

    def get_photo_count(self):
        return len(self.photos_conf["before"]) + len(self.photos_conf["after"])

    class Meta:
        verbose_name = 'Номинация'
        verbose_name_plural = 'Номинации'
        ordering = ['id']

    def __str__(self):
        return self.name


class NominationAttribute(models.Model):
    name = models.CharField(max_length=150)
    nomination = models.ForeignKey('Nomination', models.PROTECT, related_name='attribute')
    max_score = models.IntegerField(default=5)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50,
                            help_text='Введите название мероприятия',
                            verbose_name='Название мероприятия')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.ForeignKey('users.User', models.PROTECT)
    event = models.ForeignKey('Event', models.PROTECT)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self) -> str:
        return f"Участник {self.user} в мероприятии {self.event}"


class EventStaff(models.Model):
    user = models.ForeignKey('users.User', models.PROTECT)
    category_nomination = models.ForeignKey('CategoryNomination', models.PROTECT, default=1, related_name='staffs')

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'

    def __str__(self) -> str:
        return f"Судья {self.user} в мероприятии {self.category_nomination}"


class EventCategory(models.Model):
    event = models.ForeignKey('Event', models.PROTECT)
    category = models.ForeignKey('Category', models.PROTECT)

    class Meta:
        verbose_name = 'Категории мероприятия'
        verbose_name_plural = 'Категории мероприятий'

    def __str__(self) -> str:
        return f"{self.event} --- {self.category}"


class CategoryNomination(models.Model):
    event_category = models.ForeignKey('EventCategory', models.PROTECT)
    nomination = models.ForeignKey('Nomination', models.PROTECT, related_name='nom')

    class Meta:
        verbose_name = 'Номинации категорий'
        verbose_name_plural = 'Номинации категорий'

    def __str__(self) -> str:
        return f"{self.event_category} --- {self.nomination}"


class MemberNomination(models.Model):
    member = models.ForeignKey('Member', models.PROTECT, related_name='membernom')
    category_nomination = models.ForeignKey('CategoryNomination', models.PROTECT, related_name='categ')

    class Meta:
        verbose_name = 'Номинация участника'
        verbose_name_plural = 'Номинации участника'

    @property
    def is_done(self):
        count_referee = self.category_nomination.staffs.count()
        count_results = self.results.count()
        return count_results == count_referee

    def __str__(self) -> str:
        return f"{self.member} --- {self.category_nomination}"


class MemberNominationPhoto(models.Model):
    BEFORE = 'BE'
    AFTER = 'AF'
    BEFORE_AFTER_CHOICES = [
        (BEFORE, 'До'),
        (AFTER, 'После'),
    ]

    member_nomination = models.ForeignKey("MemberNomination", models.PROTECT, related_name='photos', default=None)
    photo = models.ImageField()
    before_after = models.CharField(max_length=2, choices=BEFORE_AFTER_CHOICES)

    def __str__(self) -> str:
        return f"{self.member_nomination}"



class Result(models.Model):
    membernomination = models.ForeignKey('MemberNomination', models.PROTECT, related_name='results')
    score = models.IntegerField()
    eventstaff = models.ForeignKey('EventStaff', models.PROTECT)
    score_retail = models.JSONField(default=None, null=True)


    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = [constraints.UniqueConstraint("membernomination", "eventstaff", name="unique_lower_name_category")]

    def __str__(self) -> str:
        return f"{self.score} --- {self.membernomination}"
