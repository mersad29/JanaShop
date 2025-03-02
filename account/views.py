from random import randint
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.views import View
from django.views.generic import UpdateView
from cart.models import Order
from . import forms
from .forms import AuthenticationForm, CheckOtpForm, AddressForm, ChangePasswordForm, SetPassword, EditProfileForm, \
    ChangePhoneForm
from .models import Otp, CustomUser, Address


class RegisterOrLogin(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = AuthenticationForm()
            return render(request, 'account/Register-Login.html', {'form': form})
        else:
            return render(request, 'account/profile.html')

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
        if not request.user.is_authenticated:
            form = CheckOtpForm()
            return render(request, 'account/Check-Otp.html', {'form': form})
        else:
            return render(request, 'account/profile.html')

    def post(self, request):
        form = CheckOtpForm(request.POST)
        token = request.GET.get('token')
        if form.is_valid():
            cd = form.cleaned_data

            if Otp.objects.get(token=token):
                otp = Otp.objects.get(token=token)
                if Otp.objects.filter(token=token, code=cd['code']).exists():
                    if otp.is_expired():
                        user, is_created = CustomUser.objects.get_or_create(phone=otp.phone)
                        otp.delete()
                        login(request, user)
                        return redirect('/')
                    else:
                        messages.error(request, 'کد منقضی شده است')
                else:
                    messages.error(request, 'کد اشتباه است')
            else:
                messages.error(request, 'کد اشتباه است')
        return render(request, 'account/Check-Otp.html', {'form': form})


def profile(request):
    order = Order.objects.filter(user=request.user, is_paid=True).order_by('-paid_time').first()
    return render(request, 'account/profile.html', {'order': order})


def factors(request):
    orders = Order.objects.filter(user=request.user).order_by('-paid_time')
    return render(request, 'account/factors.html', {'factors': orders})

class FactorDetailView(View):
    def get(self, request, pk):
        factor = Order.objects.get(user=request.user, id=pk)
        return render(request, 'account/factor_detail.html', {'factor': factor})


def user_logout(request):
    logout(request)
    return redirect('/')


class AddressView(View):
    def get(self, request):
        form = AddressForm()
        addresses = request.user.useraddress.all()
        contex = {
            'form': form,
            "addresses": addresses
        }
        return render(request, 'account/address_list.html', contex)


class AddAddressView(View):
    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            if not request.user.useraddress.filter(is_default=True).exists():
                address.is_default = True
            address.save()

        return redirect('account:address_list')

    def get(self, request):
        form = AddressForm()
        addresses = request.user.useraddress.all()
        contex = {
            'form': form,
            "addresses": addresses
        }
        return render(request, 'account/add_address.html', contex)


class EditAddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'account/edit_address.html'
    success_url = reverse_lazy('account:address_list')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'account/edit_profile.html', {'form': form, 'user': user})


class Set_default_address(View):
    def get(self, request, id):
        address = get_object_or_404(Address, id=id, user=request.user)
        Address.objects.filter(user=request.user).update(is_default=False)
        address.is_default = True
        address.save()
        order_id = request.session['order_id']
        return redirect(reverse('cart:checkout', args=[order_id]))

    def save(self):
        self.get.modified = True


def delete_address(request, id):
    address = get_object_or_404(Address, user=request.user, id=id)
    was_default = address.is_default
    address.delete()

    if was_default:
        remain_address = request.user.useraddress.all()
        if remain_address.exists():
            new_default = remain_address.first()
            new_default.is_default = True
            new_default.save()

    return redirect('account:address_list')


def change_password(request):
    if request.method == 'POST':
        if request.user.password is not None:
            form = ChangePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                new_password = form.cleaned_data.get('new_password')
                request.user.password = new_password
                form.save()
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
                login(request, request.user)
        else:
            form = SetPassword(data=request.POST, user=request.user)
            if form.is_valid():
                password = form.cleaned_data.get('password')
                request.user.password = password
                form.save()
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
                login(request.user)
    else:
        if request.user.is_authenticated:
            if request.user.password:
                form = ChangePasswordForm(request.user)
            else:
                form = SetPassword(request.user)

    return render(request, 'account/change_password.html', {'form': form})

def change_phone(request):
    form = ChangePhoneForm()
    if request.method == 'POST':
        form = ChangePhoneForm(request.POST)
        if form.is_valid():
            rand_code = randint(1000, 9999)
            print(rand_code)
            cd = form.cleaned_data
            token = str(uuid4())
            Otp.objects.create(phone=cd['new_phone'], token=token, code=rand_code)

            return redirect(reverse('account:check_new_phone_otp') + f"?token={token}")
    return render(request, 'account/change_phone.html', {'form': form})

class NewPhoneCheckOtp(View):
    def get(self, request):
        now = timezone.now()
        if request.user.is_authenticated:
            form = CheckOtpForm
            token = request.GET.get('token')
            if Otp.objects.get(token=token):
                otp = Otp.objects.get(token=token)
                # print(otp.created_at)
            return render(request, 'account/new_phone_checkotp.html', {'form': form, 'otp': otp, 'now': now})

        else:
            return render(request, 'account/Register-Login.html')

    def post(self, request):
        form = CheckOtpForm(request.POST)
        token = request.GET.get('token')

        if form.is_valid():
            cd = form.cleaned_data

            if Otp.objects.get(token=token):
                otp = Otp.objects.get(token=token)
                if Otp.objects.filter(token=token, code=cd['code']).exists():
                    if otp.is_expired():
                        request.user.phone = otp.phone
                        request.user.save()
                        otp.delete()
                        messages.success(request, 'شماره همراه تغییر کرد.')
                    else:
                        form.add_error('code', 'کد منقضی شده است')
                else:
                    form.add_error('code', 'کد اشتباه است')
            else:
                form.add_error('code', 'کد اشتباه است')

        return render(request, 'account/new_phone_checkotp.html', {'form': form})

def resend_code(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            rand_code = randint(1000, 9999)
            print(rand_code)
            token = str(uuid4())
            phone = request.POST.get('new_phone')
            Otp.objects.create(code=rand_code, token=token, phone=phone)

            return redirect(reverse('account:check_new_phone_otp') + f"?token={token}")
