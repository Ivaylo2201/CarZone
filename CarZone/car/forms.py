from django import forms

from .models import Car, Feature
from .choices import ORDERING


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
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
            required=False,
        )
        self.fields['images'] = MultipleFileField()

    class Meta:
        model = Car
        exclude = ('views', 'dealer', 'manufacturer', 'features')

        error_messages = {
            'horsepower': {
                'max_value': 'Ensure horsepower does not exceed 750!',
            },
            'capacity': {
                'max_value': 'Ensure capacity does not exceed 7500!',
            },
            'mileage': {
                'max_value': 'Ensure mileage does not exceed 750 000!',
            },
        }


class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = (
            'dealer',
            'views',
            'manufacturer',
            'features',
            'is_available',
            'posted_on',
        )


class CarFilterForm(forms.Form):
    brand = forms.CharField(required=False, max_length=Car.BRAND_MAX_LENGTH)
    model = forms.CharField(required=False, max_length=Car.MODEL_MAX_LENGTH)
    min_price = forms.IntegerField(required=False, min_value=0)
    max_price = forms.IntegerField(required=False, min_value=0)
    min_horsepower = forms.IntegerField(required=False, min_value=0)
    max_horsepower = forms.IntegerField(required=False, min_value=0)
    min_mileage = forms.IntegerField(required=False, min_value=0)
    max_mileage = forms.IntegerField(required=False, min_value=0)
    min_capacity = forms.IntegerField(required=False, min_value=0)
    max_capacity = forms.IntegerField(required=False, min_value=0)
    order_by = forms.ChoiceField(required=False, choices=ORDERING)
