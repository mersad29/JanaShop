from django import forms

class Discount_code(forms.Form):
    discode = forms.CharField(
        label='کد تخفیف خود را وارد کنید',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'کد تخفیف'}
        )
    )
