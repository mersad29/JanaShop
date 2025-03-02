from django import forms
from django.core.exceptions import ValidationError
from account.models import Address, CustomUser


def validate_phone_number(value):
    value = value.strip()
    if len(value) == 11:
        if not value.startswith('0'):
            raise ValidationError('لطفا یک شماره تلفن معتبر وارد کنید')
    elif len(value) == 10:
        if not value.startswith('9'):
            raise ValidationError('لطفا یک شماره تلفن معتبر وارد کنید')
    else:
        raise ValidationError('لطفا یک شماره تلفن معتبر وارد کنید')


class AuthenticationForm(forms.Form):
    phone = forms.CharField(
        validators=[validate_phone_number],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}))

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if len(phone) == 11:
    #         if phone[0] != 0:
    #             raise ValidationError("--")
    #     if not len(phone) == 11 or 10:
    #         raise ValidationError("لطفا یک شماره تلفن معتبر وارد کنید", code="phone_validation")
    #     return phone


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        print(new_password, confirm_password)
        if new_password != confirm_password:
            self.add_error('confirm_password', "رمز عبور با تکرار رمز عبور همخوانی ندارد")

        return cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password != self.user.password:
            raise ValidationError(
                ("رمز عبور فعلی شما اشتباه است"),
                code='invalid_password',
            )
        # return old_password

    def save(self):
        self.user.save()


class SetPassword(forms.Form):
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self):
        self.user.save()


class ChangePhoneForm(forms.Form):
    new_phone = forms.IntegerField(label='شماره تلفن جدید', widget=forms.NumberInput(attrs={'class': 'form-control'}))


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

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('fname', 'lname', 'telephone', 'email', 'date_of_birth',
                  'card_number', 'national_code')