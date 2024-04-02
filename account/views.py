from random import randint
from uuid import uuid4
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import AuthenticationForm, CheckOtpForm
from .models import Otp, CustomUser


class RegisterOrLogin(View):
    def get(self, request):
        form = AuthenticationForm(request.GET)
        return render(request, 'account/Register-Login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            rand_code = randint(1000, 9999)
            cd = form.cleaned_data
            print(rand_code)
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=rand_code, token=token)
            return redirect(reverse('account:check_otp') + f"?token={token}")

        return render(request, 'account/Register-Login.html', {'form': form})

class CheckOtp(View):
    def get(self, request):
        form = CheckOtpForm(request.GET)
        return render(request, 'account/Check-Otp.html', {'form': form})

    def post(self, request):
        form = CheckOtpForm(request.POST)
        token = request.GET.get('token')
        if form.is_valid():
            cd = form.cleaned_data
            otp = Otp.objects.get(token=token)
            if Otp.objects.filter(token=token, code=cd['code']).exists():
                    user, is_created = CustomUser.objects.get_or_create(phone=otp.phone)
                    login(request, user)
            otp.delete()
            return redirect('/')
        return render(request, 'account/Check-Otp.html', {'form': form})

def profile(request):
    return render(request, 'account/profile.html')

def user_logout(request):
    logout(request)
    return redirect('/')