from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.db import models


class User(AbstractUser):
    image = ResizedImageField(size=[500, 300], quality=75, upload_to='images/', null=True, blank=True)

    phone_number = models.CharField(max_length=11,
                                    help_text="Введите номер телефона пользователя",
                                    verbose_name="Номер телефона")

    REQUIRED_FIELDS = ["phone_number"]

    class Meta(AbstractUser.Meta):
        pass

    def save(self, *args, **kwargs):
        self.username = self.phone_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name[0]}.'
