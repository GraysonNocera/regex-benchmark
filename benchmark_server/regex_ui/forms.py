import copy
import json

from django import forms

from .constants import AVAILABLE_TEXT_FILES, ENGINES


class DynamicMultipleChoiceField(forms.MultipleChoiceField):     
    def clean(self, value):
        return value

class BenchmarkForm(forms.Form):
    name = forms.CharField(label='Test Name', required=True, max_length=100)
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea)
    test_regexes = DynamicMultipleChoiceField(label='Regex', required=True)
    test_string_files = forms.MultipleChoiceField(label='Text File Name', required=True, choices=[(file, file) for file in AVAILABLE_TEXT_FILES])
    engines = forms.MultipleChoiceField(label='Engines', required=True, choices=[(engine, engine) for engine in ENGINES])
    run_times = forms.IntegerField(label='Run Times', required=True, initial=10)
    split_string_file = forms.BooleanField(label='Split String File', required=False, initial=False)
    regexes_in_file = forms.BooleanField(label='Regexes in File', required=False, initial=False)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['name'].startswith('test_'):
            cleaned_data['name'] = 'test_' + cleaned_data['name']
        return cleaned_data
    
    def to_json(self):
        data = {
            'name': self.cleaned_data['name'],
            'test_regexes': self.cleaned_data['test_regexes'],
            'description': self.cleaned_data['description'],
            'test_string_files': self.cleaned_data['test_string_files'],
            'run_times': self.cleaned_data['run_times'],
            'engines': self.cleaned_data['engines'],
            'split_string_file': self.cleaned_data['split_string_file'],
            'regexes_in_file': self.cleaned_data['regexes_in_file']
        }
        return json.dumps([data], indent=4)

    def from_json(json_data):
        if isinstance(json_data, dict):
            data = copy.deepcopy(json_data)
        else:
            data = json.loads(json_data)
        
        data['test_regexes'] = [(regex, regex) for regex in data.get('test_regexes', [])]
        data['test_string_files'] = [(file, file) for file in data.get('test_string_files', [])]
        data['engines'] = [(engine, engine) for engine in data.get('engines', [])]
        # print(data)
        return BenchmarkForm(initial=data, data=None)
    

if __name__ == '__main__':
    json_data = '{"name": "Modified Test Form", "description": "Modified test description", "engines": ["Java"]}'
    form = BenchmarkForm.from_json(json_data)
    if form.is_valid():
        print(form.cleaned_data)
    else:
        pass
        