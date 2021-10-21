from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Reg
from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.validators import RegexValidator


class RegModelForm(forms.ModelForm):
	user_name = forms.CharField(
		label='',
		widget=forms.TextInput(
			attrs={
				'id': 'username',
				'class': 'form-control form-control-lg mb-3',
				'placeholder': 'Имя Фамилия',
				'autocomplete':'off',
				'data-inputmask-regex': r'^[A-zА-я ]+$'
			}
		)
	)
	phone_num = forms.CharField(
		label='',
		widget=forms.TextInput(
			attrs={
				'type': 'tel',
				'id': 'reg_tel',
				'class': 'form-control form-control-lg mb-3',
				'placeholder': '+998 (__) ___-__-__',
				'autocomplete':'off',
				'data-inputmask-regex': r'^\+998 \([0-9]{2}\) [0-9]{3}-[0-9]{2}-[0-9]{2}$'
			}
		)
	)

	class Meta:
		model = Reg
		fields = ['user_name', 'phone_num']
