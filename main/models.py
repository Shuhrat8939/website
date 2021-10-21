from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.core.validators import RegexValidator
from django import forms
from solo.models import SingletonModel
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField

import random


class LimitedImageField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        self.min_dim = kwargs.pop('min_dim', None)
        self.max_dim = kwargs.pop('max_dim', None)
        self.dim_limit = kwargs.pop('dim_limit', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.FILE_UPLOAD_MAX_MEMORY_SIZE
        super(LimitedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(LimitedImageField, self).clean(*args, **kwargs)
        try:
            img_file = data.file
            if img_file.size > self.max_upload_size:
                err_msg = 'Размер файла не должен превышать {}'.format(filesizeformat(self.max_upload_size))
                raise forms.ValidationError(err_msg)

            w, h = get_image_dimensions(img_file)
            if self.dim_limit:
                if (w != self.dim_limit[0]) or (h != self.dim_limit[1]):
                    err_msg = 'Разрешение изображения должно быть {}x{}'.format(*self.dim_limit)
                    raise forms.ValidationError(err_msg)
            if self.min_dim:
                if (w < self.min_dim[0]) or (h < self.min_dim[1]):
                    err_msg = 'Разрешение изображения не должно быть меньше, чем {}x{}'.format(*self.min_dim)
                    raise forms.ValidationError(err_msg)
            if self.max_dim:
                if (w > self.max_dim[0]) or (h > self.max_dim[1]):
                    err_msg = 'Разрешение изображения не должно превышать {}x{}'.format(*self.max_dim)
                    raise forms.ValidationError(err_msg)
        except AttributeError:
            pass
        return data


class Menu(models.Model):
	title = models.CharField(max_length=50, verbose_name='Названия')
	desc = models.TextField(blank=False, max_length=100, verbose_name='Краткое описание')
	full_desc = RichTextUploadingField(blank=True, verbose_name='Полное описание')
	img = models.ImageField(upload_to="images/%Y/%M/%d/", verbose_name='Фото')
	price = models.PositiveIntegerField(verbose_name='Цена')
	time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
	time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
	is_published = models.BooleanField(default=True, verbose_name='Публикатция')
	is_new = models.BooleanField(default=False, verbose_name='Новинки')
	is_recom = models.BooleanField(default=False, verbose_name='Рекомендуемые')
	cat = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, verbose_name='Категория')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post', kwargs={'post_id': self.pk})

	class Meta:
		verbose_name = "Меню"
		verbose_name_plural = "Меню"
		ordering = ['-time_create', 'title']


class Category(models.Model):
	title = models.CharField('Категория', max_length=50, db_index=True)
	dropdown = models.ForeignKey('Dropdown', on_delete=models.CASCADE, null=True, verbose_name="Dropdown")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('category', kwargs={'cat_id': self.pk})

	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"


class Dropdown(models.Model):
	title = models.CharField('Dropdown', max_length=50, db_index=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('dropdown', kwargs={'dropdown_id':self.pk})

	class Meta:
		verbose_name = "Dropdown"
		verbose_name_plural = "Dropdown"


class Sales(models.Model):
	title = models.CharField('Заголовок', max_length=50, db_index=True)
	text = RichTextUploadingField(blank=True, verbose_name='Текст')
	banner = LimitedImageField(dim_limit=(1200,360), upload_to="banner/%Y/%M/%d/", verbose_name='Фото')
	time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
	time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
	date = models.DateField(auto_now=True)
	view_in_slider = models.BooleanField(default=False, verbose_name='Отображать в слайдере')
	is_published = models.BooleanField(default=True, verbose_name='Публикатция')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('sale', kwargs={'sale_id':self.pk})

	class Meta:
		verbose_name = "Акция"
		verbose_name_plural = "Акции"


class Slider(models.Model):
	title = models.CharField('Заголовок', max_length=50, db_index=True)
	banner = LimitedImageField(dim_limit=(1200,360), upload_to="banner/%Y/%M/%d/", verbose_name='Фото')
	url = models.URLField(blank=True, verbose_name='URL')
	is_published = models.BooleanField(default=True, verbose_name='Публикатция')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('slider', kwargs={'slider_id':self.pk})

	class Meta:
		verbose_name = "Слайдер"
		verbose_name_plural = "Слайдер"


class NewsPage(models.Model):
	title = models.CharField('Заголовок', max_length=50, db_index=True)
	img = LimitedImageField(blank=True, dim_limit=(1200,360), upload_to="banner/%Y/%M/%d/", verbose_name='Фото')
	desc = models.TextField(blank=True, max_length=100, verbose_name='Краткое описание')
	body = RichTextUploadingField(blank=True, null=True, verbose_name="Контент:")
	date = models.DateField(auto_now=True)
	is_published = models.BooleanField(default=True, verbose_name='Публикатция')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("shownews", kwargs={'shownews_id': self.pk})

	class Meta:
		verbose_name='Новости'
		verbose_name_plural='Новости'


class AboutPage(SingletonModel):
	body = RichTextUploadingField(blank=True, null=True, verbose_name="Контент:")

	class Meta:
		verbose_name='О нас'
		verbose_name_plural='О нас'


class DeliveryPage(SingletonModel):
	banner = LimitedImageField(blank=True, dim_limit=(1200,360), upload_to="banner/%Y/%M/%d/", verbose_name='Фото:')
	body = RichTextUploadingField(blank=True, null=True, verbose_name="Контент:")

	class Meta:
		verbose_name='Доставка'
		verbose_name_plural='Доставка'


class ContactsPage(SingletonModel):
	yandex_map = models.BooleanField(default=True, verbose_name='Яндекс Карта:')
	body = RichTextUploadingField(blank=True, null=True, verbose_name="Контент:")

	class Meta:
		verbose_name='Контакты'
		verbose_name_plural='Контакты'


class Contacts_and_links(SingletonModel):
	logo_choices = [
		('fab fa-facebook-f', 'Facebook'),
		('fab fa-telegram', 'Telegram'),
		('fab fa-google', 'Google'),
		('fab fa-instagram', 'Instagram'),
		('fab fa-discord', 'Discord'),
		('fab fa-vk', 'VK'),
		('fab fa-google-play', 'Google Play'),
		('fab fa-linkedin', 'Linkedin'),
		('fas fa-link', 'Link'),
		('fab fa-app-store', 'App Store'),
		('fab fa-whatsapp', 'WhatsApp'),
		('fab fa-yandex-international', 'Yandex'),
		('fab fa-github', 'GitHub'),
		('fas fa-vr-cardboard', 'VR'),
		('fas fa-robot', 'Robot'),
	]

	phone_num = PhoneNumberField(verbose_name='Телефон номер:', validators=[RegexValidator(r'^\+\d{3}\d{2}\d{3}\d{2}\d{2}$')])
	comment = models.CharField(verbose_name='Текст:', default='Ежедневно с 09:00 до 21:00', max_length=30)
	
	icon_1 = models.CharField(blank=True, choices=logo_choices, max_length=100, verbose_name="Иконка:")
	color_1 = ColorField(blank=True, default='#FF0000', verbose_name="Цвет:")
	link_1 = models.URLField(blank=True, verbose_name="URL:")
	
	icon_2 = models.CharField(blank=True, choices=logo_choices, max_length=100, verbose_name="Иконка:")
	color_2 = ColorField(blank=True, default='#FF0000', verbose_name="Цвет:")
	link_2 = models.URLField(blank=True, verbose_name="URL:")
	
	icon_3 = models.CharField(blank=True, choices=logo_choices, max_length=100, verbose_name="Иконка:")
	color_3 = ColorField(blank=True, default='#FF0000', verbose_name="Цвет:")
	link_3 = models.URLField(blank=True, verbose_name="URL:")
	
	icon_4 = models.CharField(blank=True, choices=logo_choices, max_length=100, verbose_name="Иконка:")
	color_4 = ColorField(blank=True, default='#FF0000', verbose_name="Цвет:")
	link_4 = models.URLField(blank=True, verbose_name="URL:")

	class Meta:
		verbose_name = 'Контакты и ссылки'
		verbose_name_plural = 'Контакты и ссылки'


class Reg(models.Model):
	user_name = models.CharField(
		max_length=50,
		verbose_name='Ф.И.Ш',
		validators=[
			RegexValidator(r'^[A-zА-я ]+$')
		]
	)

	phone_num = models.CharField(
		max_length=20,
		verbose_name='Телефон номер:',
		validators=[
			RegexValidator(r'^\+998 \([0-9]{2}\) [0-9]{3}-[0-9]{2}-[0-9]{2}$')
		]
	)


	def __str__(self):
		return self.user_name

	def get_absolute_url(self):
		return reverse("user", kwargs={'user_id': self.pk})


	class Meta:
		verbose_name = 'Пользователь сайта'
		verbose_name_plural = 'Пользователи сайта'


class BotSetting(SingletonModel):
	chat_id = models.CharField(
		max_length=20,
		verbose_name="Чат ID:",
		default='1134693533'
	)

	class Meta:
		verbose_name = 'Настройки бота'
		verbose_name_plural = 'Настройки бота'