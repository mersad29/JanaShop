from django import forms

from product.models import Discount


class Discount_code(forms.Form):
    code = forms.CharField(
        label='کد تخفیف خود را وارد کنید',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'کد تخفیف'}
        )
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            discount = Discount.objects.get(code=code, is_active=True)
            if not discount.is_valid():
                raise forms.ValidationError("این کد تخفیف منقضی شده است.")
        except Discount.DoesNotExist:
            raise forms.ValidationError("کد تخفیف نامعتبر است.")
        return code

