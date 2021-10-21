from django.contrib import admin
from .models import Menu, Category, Dropdown, Sales, Slider, AboutPage, NewsPage, DeliveryPage, ContactsPage, Contacts_and_links, Reg, BotSetting
from solo.admin import SingletonModelAdmin
from django.utils.safestring import mark_safe

# Register your models here.

admin.site.site_title = "SAKURA SUSHI UZ"
admin.site.site_header = "SAKURA SUSHI UZ"


class RegAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_name', 'phone_num')
	list_display_links = ('id', 'user_name')

class MenuAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'cat', 'price', 'time_create', 'time_update', 'get_html_img', 'is_new', 'is_recom', 'is_published')
	list_display_links = ('id', 'title')
	search_fields = ('title', 'desc')

	def get_html_img(self, object):
		if object.img:
			return mark_safe(f"<a href='{object.img.url}'><img src='{object.img.url}' width=50></a>")

	get_html_img.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'dropdown', 'dropdown_id')


class DropdownAdmin(admin.ModelAdmin):
	list_display = ('id', 'title')


class SalesAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'time_create', 'time_update', 'banner', 'view_in_slider', 'is_published')
	list_display_links = ('id', 'title')

class SliderAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'banner', 'url', 'is_published')
	list_display_links = ('id', 'title')

class NewsPageAdmin(admin.ModelAdmin):
	list_display = ('id', 'title','is_published')
	list_display_links = ('id', 'title')

class Contacts_and_linksAdmin(SingletonModelAdmin):
	fieldsets = (
		('Телефон номер', {
			'fields': ('phone_num', 'comment')
		}),
		('Ссылка 1', {
			'fields': ('icon_1', 'color_1', 'link_1')
		}),
		('Ссылка 2', {
			'fields': ('icon_2', 'color_2', 'link_2')
		}),
		('Ссылка 3', {
			'fields': ('icon_3', 'color_3', 'link_3')
		}),
		('Ссылка 4', {
			'fields': ('icon_4', 'color_4', 'link_4')
		}),
	)

#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Dropdown, DropdownAdmin)
admin.site.register(Reg, RegAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(NewsPage, NewsPageAdmin)
admin.site.register(AboutPage, SingletonModelAdmin)
admin.site.register(DeliveryPage, SingletonModelAdmin)
admin.site.register(ContactsPage, SingletonModelAdmin)
admin.site.register(Contacts_and_links, Contacts_and_linksAdmin)
admin.site.register(BotSetting, SingletonModelAdmin)