from .models import Contacts_and_links

def contacts(request):
	get_data = Contacts_and_links.objects.all()
	
	data = {
		'tel': get_data[0].phone_num,
		'comment': get_data[0].comment,

		'icon_1': get_data[0].icon_1,
		'color_1': get_data[0].color_1,
		'link_1': get_data[0].link_1,

		'icon_2': get_data[0].icon_2,
		'color_2': get_data[0].color_2,
		'link_2': get_data[0].link_2,

		'icon_3': get_data[0].icon_3,
		'color_3': get_data[0].color_3,
		'link_3': get_data[0].link_3,

		'icon_4': get_data[0].icon_4,
		'color_4': get_data[0].color_4,
		'link_4': get_data[0].link_4
	}
	return data