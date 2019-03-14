# -*- coding: utf-8 -*-

from django import forms

from .models import Contact
import pdb # pdb.set_trace()

class ContactForm(forms.ModelForm):

    files = forms.ImageField(label=False, widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


    class Meta:
        model = Contact
        fields = ('name', 'phone', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Номер телефона. Обязательно'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'body': forms.Textarea(
                attrs={'placeholder': 'Текст сообщения. Обязательно'}),
            }
        labels = {
            'name': False,
            'phone': False,
            'email': False,
            'body': False,
            }

        css = { 'all': ('contact/contact.css',)}
        js = ('animations.js', 'actions.js')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                })
