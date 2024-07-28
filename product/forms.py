from django import forms

class ProductFilterForm(forms.Form):
    sort_choice = [
        ('newest', 'Newest'),
        ('greatest', 'Greatest'),
        ('most_popular', 'Most Popular'),
    ]
    category = forms.CharField(required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    in_stoke = forms.BooleanField(required=False)
    sort_by = forms.ChoiceField(choices=sort_choice, required=False)