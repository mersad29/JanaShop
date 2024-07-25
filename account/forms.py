from django import forms
from django.core.exceptions import ValidationError
from account.models import Address


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

class AddressForm(forms.ModelForm):
    choices = [
        ('tehran', 'تهران'),
        ('alborz', 'البرز'),
        ('isfahan', 'اصفهان'),
        ('fars', 'فارس'),
        ('khorasan_razavi', 'خراسان رضوی'),
        ('khuzestan', 'خوزستان'),
        ('mazandaran', 'مازندران'),
        ('east_azarbaijan', 'آذربایجان شرقی'),
        ('west_azarbaijan', 'آذربایجان غربی'),
        ('gilan', 'گیلان'),
        ('hamadan', 'همدان'),
        ('kermanshah', 'کرمانشاه'),
        ('markazi', 'مرکزی'),
        ('qom', 'قم'),
        ('semnan', 'سمنان'),
        ('sistan_baluchestan', 'سیستان و بلوچستان'),
        ('yazd', 'یزد'),
        ('ardebil', 'اردبیل'),
        ('chaharmahal_bakhtiari', 'چهارمحال و بختیاری'),
        ('golestan', 'گلستان'),
        ('hamedan', 'همدان'),
        ('hormozgan', 'هرمزگان'),
        ('ilam', 'ایلام'),
        ('kerman', 'کرمان'),
        ('kurdistan', 'کردستان'),
        ('lorestan', 'لرستان'),
        ('qazvin', 'قزوین'),
        ('kohgiluyeh_boyer_ahmad', 'کهگیلویه و بویراحمد'),
        ('north_khorasan', 'خراسان شمالی'),
        ('south_khorasan', 'خراسان جنوبی'),
        ('bushehr', 'بوشهر'),
        ('zanjan', 'زنجان')
    ]


    state = forms.ChoiceField(choices=choices)
    user = forms.IntegerField(required=False)
    class Meta:
        model = Address
        fields = ('state', 'city', 'name', 'address', 'postal_code', 'phone')