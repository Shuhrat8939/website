from django.shortcuts import render, get_object_or_404
from .models import Menu, Category, Dropdown, Sales, Slider, NewsPage, AboutPage, DeliveryPage, ContactsPage, Reg, BotSetting
from django.template.defaulttags import register
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import redirect

from django.urls import reverse_lazy
from .forms import RegModelForm
from bootstrap_modal_forms.generic import BSModalCreateView

import re
from django.core.exceptions import ValidationError

from django.template.loader import render_to_string
from django.http import JsonResponse

import random
import json

from .sms import send_sms
from .bot import send_order


@register.filter
def get_range(value):
	return range(value)

@register.filter
def fixed_price(value):
	val = ''
	v = str(value)[::-1]

	counter = 0

	for i in v:
		val += i
		counter += 1

		if counter == 3:
			val += ' '
			counter = 0

	return val[::-1]

@register.filter
def phone_num(value):
	value = str(value)

	return f"{value[:4]} {value[4:6]} {value[6:9]}-{value[9:11]}-{value[11:]}" 


def index(request):
	menu = Menu.objects.all()
	category = Category.objects.all()

	a = Slider.objects.all()
	b = Sales.objects.all()

	length = 0
	active = None
	active_type = None

	slider = []

	for i in a:
		if i.is_published:
			length += 1
			if length == 1:
				active = i
				active_type = 'slider'
			else:
				slider.append(i)

	sales = []

	for i in b:
		if i.is_published and i.view_in_slider:
			length += 1
			if length == 1:
				active = i
				active_type = 'sales'
			else:
				sales.append(i)

	recom = False

	for i in menu:
		if i.is_published and i.is_recom:
			recom = True
			break

	new = False

	for i in menu:
		if i.is_published and i.is_new:
			new = True
			break

	x = {}
	for C in category:
		y = []
		for M in menu.filter(cat_id__exact=C.id):
			y.append(M)

		if len(y) == 0:
			continue
		
		x[C] = y


	data = {
		"length": length,
		"active": active,
		"active_type": active_type,
		"slider": slider,
		"sales": sales,
		"menu": menu,
		"recom": recom,
		"new": new,
		"foods": x
	}

	return render(request, "main/index.html", data)


def LoginView(request):
	data = dict()
	if request.method == 'POST':
		print(f"login: {request.POST['phone_num']}")

		obj = Reg.objects.all()
		phone_num = request.POST['phone_num']

		if obj.filter(phone_num__exact=phone_num).exists():
			user = obj.filter(phone_num__exact=phone_num)

			data['form_is_valid'] = True
			
			data['user_data'] = {
				'username': user[0].user_name,
				'phone_number': user[0].phone_num
			}

		else:
			data['form_is_valid'] = False

	data['html_form'] = render_to_string('main/login.html', request=request)
	return JsonResponse(data)


def RegisterView(request):
	data = dict()
	if request.method == 'POST':
		form = RegModelForm(request.POST)
		if form.is_valid():

			obj = Reg.objects.all()
			phone_num = request.POST.get('phone_num')

			if obj.filter(phone_num__exact=phone_num).exists():
				data['form_is_valid'] = False
				data['form_error_text'] = 'Такой контакт уже существует!'

			else:
				user = form.save()

				data['form_is_valid'] = True

				data['user_data'] = {
					'username': user.user_name,
					'phone_number': user.phone_num
				}

		else:
			data['form_is_valid'] = False
			print(form.errors)

	else:
		form = RegModelForm()

	context = {
		'form': form
	}

	data['html_form'] = render_to_string('main/register.html', context, request=request)
	return JsonResponse(data)


def CheckoutView(request):
	data = dict()
	if request.method == 'GET':
		user = request.GET.copy()

		menu = Menu.objects.all()

		order = {
			'full_name': user['user[username]'],
			'tel': user['user[phone_number]'],
			'order': {}
		}

		del user['user[username]']
		del user['user[phone_number]']

		for key, value in user.items():
			i = key.replace('product[', '').replace(']', '')

			order['order'][i] = {
				'name': menu.get(id=int(i)).title,
				'count': int(value),
				'price': menu.get(id=int(i)).price
			}

		chat_id = BotSetting.objects.all()

		send_order(chat_id=chat_id[0].chat_id, data=order)
	

	data['is_success'] = True

	return JsonResponse(data)


def menu(request):
	menu = Menu.objects.all()
	category = Category.objects.all()

	dropdown = [
		Dropdown.objects.get(id=2),
		Dropdown.objects.get(id=3),
		Dropdown.objects.get(id=1)
	]

	data = {}

	for D in dropdown:
		x = {}

		for C in category.filter(dropdown_id__exact=D.id):
			y = []

			for M in menu.filter(cat_id__exact=C.id):
				y.append(M)

			x[C] = y

		data[D] = x

	new = menu.filter(is_published__exact=1).filter(is_new=1)

	return render(request, "main/menu.html", {"data": data, 'menu': menu, 'new': len(new)})


def show_product(request, post_id):
	product = get_object_or_404(Menu, pk=post_id)

	return render(request, "main/product.html", {'product': product})


def news(request):
	news = NewsPage.objects.all()

	return render(request, "main/news.html", {'news': news})


def show_news(request, shownews_id):
	news = get_object_or_404(NewsPage, pk=shownews_id)

	data = {
		'title': news.title,
		'img': news.img,
		'body': news.body
	}


	return render(request, "main/show_news.html", data)


def about(request):
	about = AboutPage.objects.all()

	return render(request, "main/about.html", {'about': about[0].body})


def sales(request):
	sale = Sales.objects.all()

	data = {
		'sales': sale
	}

	return render(request, "main/sales.html", data)


def show_sales(request, sale_id):
	sale = get_object_or_404(Sales, pk=sale_id)

	data = {
		'title': sale.title,
		'text': sale.text,
		'banner': sale.banner
	}

	return render(request, 'main/sale.html', data)


def delivery(request):
	delivery = DeliveryPage.objects.all()

	data = {
		'img': delivery[0].banner,
		'body': delivery[0].body
	}

	return render(request, "main/delivery.html", data)


def contacts(request):
	contacts = ContactsPage.objects.all()

	data = {
		'yandex_map': contacts[0].yandex_map,
		'contacts': contacts[0].body
	}

	return render(request, "main/contacts.html", data)
