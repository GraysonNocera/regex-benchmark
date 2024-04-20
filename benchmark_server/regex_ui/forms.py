from django import forms

from .constants import ENGINES

class BenchmarkForm(forms.Form):
    test_name = forms.CharField(label='Test Name', max_length=100)
    regex = forms.CharField(label='Regex', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    text_file_name = forms.CharField(label='Text File Name', max_length=100)
    engines = forms.MultipleChoiceField(label='Engines', choices=[(engine, engine) for engine in ENGINES])

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation logic here
        return cleaned_data