from django.db import models
from django.conf import settings


class Users(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    users = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.SET_NULL,
                                 blank=True, null=True)


    def __str__(self):
        return f'{str(self.users)}'


class News(models.Model):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-id']

    created_date = models.TimeField('Дата создания', auto_now_add=True, null=True)
    updated_date = models.TimeField('Дата обновления', auto_now=True, null=True)
    title = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    short_description = models.CharField(verbose_name='Короткое описиние', max_length=232, blank=True, null=True)
    image = models.ImageField(verbose_name='Фото', upload_to='Фото', blank=True, null=True)
    creators = models.ForeignKey(Users, on_delete=models.SET_NULL, verbose_name='Пользователь', blank=True, null=True)

    def __str__(self):
        return f'{str(self.title)}'