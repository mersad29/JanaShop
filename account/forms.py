from django import forms
from django.core.exceptions import ValidationError


class AuthenticationForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}))

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if not len(phone) == 11:
    #         raise ValidationError("لطفا یک شماره تلفن معتبر وارد کنید", code="phone_validation")
    #     return phone
class CheckOtpForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'کد'}))