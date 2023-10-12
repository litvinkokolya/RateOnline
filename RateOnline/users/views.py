import random
import smsc_api as sms
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib import messages
from users.models import User
from .forms import UploadImageForm


def check_phone(phone: str):
    if len(phone) != 11:
        return False
    if not phone.isnumeric():
        return False
    if phone[0] not in ['7', '8']:
        return False
    return True


class LoginIn(TemplateView):
    template_name = 'users/index.html'

    def post(self, request):
        phone = request.POST.get('phone')
        if check_phone(phone):
            user = User.objects.filter(phone_number=phone).first()
            if user is None:
                messages.error(request, 'Такого пользователя нет')
                return super().get(request)
            name_user = user.first_name
            random_number = str(random.randint(1000, 9999))
            # token = sms.get_token()
            # print('token=' + token)
            # message_id = sms.send_sms(token, phone, random_number, name_user)
            # print('messageId=' + message_id)
            # status = sms.check_status(token, message_id)
            # print('status=' + status)
            print(random_number)
            user.set_password(random_number)
            user.save()
            return redirect(reverse_lazy('confirmation') + f'?phone={phone}')
        messages.error(request, 'Номер введён неверно')
        return super().get(request)


class CheckCode(TemplateView):
    template_name = 'users/confirmation.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['phone'] = self.request.GET.get('phone')
        return data

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = User.objects.filter(phone_number=phone).first()
        if user is None:
            messages.error(request, 'Такого пользователя нет')
            return super().get(request)
        if user.check_password(password):
            login(request, user)
            return redirect(reverse_lazy('photo_selection'))
        messages.error(request, 'Код введён неверно')
        return super().get(request)


class PhotoUpload(UpdateView):
    template_name = 'users/photo-selection.html'
    form_class = UploadImageForm

    def get(self, request, *args, **kwargs):
        if request.user.image:
            if self.request.user.is_staff:
                return redirect(reverse_lazy('referee_page'))
            return redirect(reverse_lazy('master_page'))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('referee_page')
        return reverse_lazy('master_page')

    def get_object(self, queryset=None):
        return self.request.user
