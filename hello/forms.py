from django import forms
from .models import Parameters
from .models import Tank

class ParametersForm(forms.ModelForm):
    class Meta:
        model = Parameters
        fields = ['temp_enabled', 'ph_enabled', 'salinity_enabled', 'ammonia_enabled', 'temp_min', 'temp_max',
                  'ph_min', 'ph_max', 'salinity_min', 'salinity_max', 'ammonia_min', 'ammonia_max']
    temp_enabled = forms.BooleanField(label='Temperature', required=False)
    ph_enabled = forms.BooleanField(label='pH', required=False)
    salinity_enabled = forms.BooleanField(label='Salinity', required=False)
    ammonia_enabled = forms.BooleanField(label='Ammonia', required=False)
    temp_min = forms.DecimalField(label='Min Temperature', required=False)
    temp_max = forms.DecimalField(label='Max Temperature', required=False)
    ph_min = forms.DecimalField(label='Min pH', required=False)
    ph_max = forms.DecimalField(label='Max pH', required=False)
    salinity_min = forms.DecimalField(label='Min Salinity', required=False)
    salinity_max = forms.DecimalField(label='Max Salinity', required=False)
    ammonia_min = forms.DecimalField(label='Min Ammonia', required=False)
    ammonia_max = forms.DecimalField(label='Max Ammonia', required=False)

    def clean(self):
        cleaned_data = super().clean()
        enabled_fields = ['temp_enabled', 'ph_enabled', 'salinity_enabled', 'ammonia_enabled']
        min_max_fields = [
            ('temp_min', 'temp_max'),
            ('ph_min', 'ph_max'),
            ('salinity_min', 'salinity_max'),
            ('ammonia_min', 'ammonia_max'),
        ]

        for i, enabled_field in enumerate(enabled_fields):
            min_field, max_field = min_max_fields[i]

            if cleaned_data.get(enabled_field):
                min_value = cleaned_data.get(min_field)
                max_value = cleaned_data.get(max_field)

                if min_value is None and max_value is None:
                    raise forms.ValidationError(f"Either min or max values for {enabled_field} must be provided when it is enabled.")

                if min_value >= max_value:
                    raise forms.ValidationError(f"The min value for {enabled_field} must be less than the max value.")




    def __init__(self, *args, **kwargs):
        self.tank = kwargs.pop('tank', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        tank_id = self.initial['tank_id']
        try:
            parameters = Parameters.objects.get(tank_id=tank_id)
        except Parameters.DoesNotExist:
            parameters = instance
            parameters.tank_id = tank_id
        else:
            parameters.temp_enabled = instance.temp_enabled
            parameters.ph_enabled = instance.ph_enabled
            parameters.salinity_enabled = instance.salinity_enabled
            parameters.ammonia_enabled = instance.ammonia_enabled
            parameters.temp_min = instance.temp_min
            parameters.temp_max = instance.temp_max
            parameters.ph_min = instance.ph_min
            parameters.ph_max = instance.ph_max
            parameters.salinity_min = instance.salinity_min
            parameters.salinity_max = instance.salinity_max
            parameters.ammonia_min = instance.ammonia_min
            parameters.ammonia_max = instance.ammonia_max

        if commit:
            parameters.save()

        return parameters