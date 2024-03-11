from django import forms

from .models import Car, Feature


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)


    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CarCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CarCreateForm, self).__init__(*args, **kwargs)
        self.fields['features'] = forms.ModelMultipleChoiceField(
            queryset=Feature.objects.all(),
            widget=forms.CheckboxSelectMultiple(),
            required=False
        )
        self.fields['images'] = MultipleFileField()

    class Meta:
        model = Car
        exclude = ('views', 'dealer', 'manufacturer', 'features')


class CarFilterForm(forms.Form):
    brand = forms.CharField(
        required=False,
        max_length=Car.BRAND_MAX_LENGTH,
        widget=forms.TextInput(attrs={'name': 'brand'})
    )
    model = forms.CharField(
        required=False,
        max_length=Car.MODEL_MAX_LENGTH,
        widget=forms.TextInput(attrs={'name': 'model'})
    )
    min_price = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'minPrice'})
    )
    max_price = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'maxPrice'})
    )
    min_horsepower = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'minHorsepower'})
    )
    max_horsepower = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'maxHorsepower'})
    )
    min_mileage = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'minMileage'})
    )
    max_mileage = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'maxMileage'})
    )
    min_capacity = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'minCapacity'})
    )
    max_capacity = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'name': 'maxCapacity'})
    )
