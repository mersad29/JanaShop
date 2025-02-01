from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the selected category (or default to None)
        if self.instance and self.instance.category:
            category_name = self.instance.category.name
        else:
            category_name = self.data.get('category', None)

        # Customize fields based on category
        if category_name == "گوشی و موبایل":
            self.fields['processor'].widget = forms.HiddenInput()
            self.fields['ram'].widget = forms.HiddenInput()
            self.fields['storage'].widget = forms.HiddenInput()
        elif category_name == "لپ تاپ":
            self.fields['screen_size'].widget = forms.HiddenInput()
            self.fields['battery_capacity'].widget = forms.HiddenInput()
        else:
            # Hide all category-specific fields by default
            self.fields['screen_size'].widget = forms.HiddenInput()
            self.fields['battery_capacity'].widget = forms.HiddenInput()
            self.fields['processor'].widget = forms.HiddenInput()
            self.fields['ram'].widget = forms.HiddenInput()
            self.fields['storage'].widget = forms.HiddenInput()
