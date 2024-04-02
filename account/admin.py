from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as UM
from account.models import CustomUser, Otp


class UserCreationForm(forms.ModelForm):
    phone = forms.CharField(label="شماره تلفن")

    class Meta:
        model = CustomUser
        fields = ["phone"]

    def clean_data(self):
        phone = self.clean_data["phone"]
        if phone.exist():
            raise ValidationError("حساب کاربری ای با این شماره وجود دارد")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        return user

# class UserAdmin(UM):
#     add_form = UserCreationForm
#
#     list_display = ["phone"]

admin.site.register(CustomUser)
admin.site.register(Otp)