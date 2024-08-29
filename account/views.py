from random import randint
from uuid import uuid4
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from .forms import AuthenticationForm, CheckOtpForm, AddressForm
from .models import Otp, CustomUser, Address


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

<<<<<<< HEAD
=======
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

>>>>>>> 1bb372e (Most off and Fire Sale(timer) - 29/8/2024 9:45 PM)
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
