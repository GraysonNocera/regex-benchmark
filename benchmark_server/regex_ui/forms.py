from django import forms

from .constants import ENGINES
import json

class BenchmarkForm(forms.Form):
    name = forms.CharField(label='Test Name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    test_regexes = forms.MultipleChoiceField(label='Regex', required=False, choices=[])
    test_string_files = forms.MultipleChoiceField(label='Text File Name', required=False, choices=[])
    engines = forms.MultipleChoiceField(label='Engines', choices=[(engine, engine) for engine in ENGINES])

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation logic here
        return cleaned_data
    
    def to_json(self):
        data = {
            'name': self.cleaned_data['name'],
            'test_regexes': self.cleaned_data['test_regexes'],
            'description': self.cleaned_data['description'],
            'test_string_files': self.cleaned_data['test_string_files'],
            'engines': self.cleaned_data['engines'],
        }
        return json.dumps(data)

    def from_json(json_data):
        if isinstance(json_data, dict):
            data = json_data
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
        