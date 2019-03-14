# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.generic import edit
from .models import Contact, Files
from django.conf import settings
from .forms import ContactForm
from django import http
import pdb # pdb.set_trace()



def send_mail(html_content, files=[]):
    subject, from_email, to = 'Заявка с сайта', settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER
    email = EmailMessage(subject, html_content, from_email, [to])
    email.content_subtype = "html"
    if files:
        for f in files:
            email.attach_file(f)
    email.send()

class ContactView(edit.FormView):

    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_invalid(self, form):
        response = super().form_invalid(form)

        if self.request.is_ajax():
            return http.JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.is_ajax():
            files = self.request.FILES.getlist('files')
            files_path = []
            id = form.save().pk
            contact = Contact.objects.get(pk=id)
            if files:
                for f in files:
                    fl = Files(contact=contact, file = f)
                    fl.save()
                    files_path.append(fl.file.path)
            data = {'message': 'Сообщение успешно отправлено.'}

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['body']

            template_email = 'contact/mail.html'
            context = {'name': name, 'mail': email, 'phone': phone, 'message': message}
            html_content = render_to_string(template_email, context)
            send_mail(html_content, files_path)
            return http.JsonResponse(data, status=200)
        else:
            return response



# class ContactView(FormView):
#     form_class = ContactForm
#     template_name = 'contact/contact.html'
#     success_url = '#' # адрес страницы успеха отправки формы


#     def post(self, request, *args, **kwargs):
#         pdb.set_trace()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('files')
#         if form.is_valid():
#             id = form.save().pk
#             contact = Contact.objects.get(pk=id)
            # if files:
            #     for f in files:
            #         fl = Files(contact=contact, file = f)
            #         fl.save()
#             data = {'message': 'Сообщение успешно отправлено.'}
#             return http.JsonResponse(data)                 #self.form_valid(form)
#         else:
#             return self.form_invalid(form)


class ContactSent(edit.CreateView):
    pass