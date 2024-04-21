import json
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import BenchmarkForm
from .constants import ENGINES, AVAILABLE_TEXT_FILES, PROJECT_ROOT


def landing_page(request):
    if request.method == 'POST':
        print(request.POST)

        form = BenchmarkForm(request.POST)
        if form.is_valid():
            test_json = form.to_json()
            # Save JSON to file
            print(os.path.join(PROJECT_ROOT, f'benchmarks/{form.cleaned_data["name"]}.json'))
            print(test_json)
            with open(os.path.join(PROJECT_ROOT, f'benchmarks/{form.cleaned_data["name"]}.json'), 'w') as file:
                file.writelines([test_json])
            return redirect('.')  # Redirect to success page after form submission
    else:
        form = BenchmarkForm()
    
    return render(request, 'regex_ui/landing.html', {'engine_list': ENGINES, "available_text_files": AVAILABLE_TEXT_FILES, "form": form})

