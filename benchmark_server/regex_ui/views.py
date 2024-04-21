import json
import os
import subprocess
import time

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .constants import AVAILABLE_TEXT_FILES, ENGINES, PROJECT_ROOT
from .forms import BenchmarkForm
from .utils import create_dir_if_not_exists


def landing_page(request):
    if request.method == 'POST':
        print(request.POST)

        form = BenchmarkForm(request.POST)
        if form.is_valid():
            test_json = form.to_json()
            test_name = form.cleaned_data['name']

            create_dir_if_not_exists(os.path.join(PROJECT_ROOT, 'benchmarks'))
            with open(os.path.join(PROJECT_ROOT, f'benchmarks/{test_name}.json'), 'w') as file:
                file.writelines([test_json])

            runbenchmark_path = os.path.join(PROJECT_ROOT, 'run-benchmarks.py')
            run_file_output = os.path.join(PROJECT_ROOT, f'runs/{test_name}_out.txt')
            run_file_error = os.path.join(PROJECT_ROOT, f'runs/{test_name}_err.txt')
            create_dir_if_not_exists(os.path.join(PROJECT_ROOT, 'runs'))

            with open(run_file_output, 'w') as file:
                with open(run_file_error, 'w') as err:
                    process = subprocess.Popen(['python3', runbenchmark_path, "test_grep.json", "10" ], stdout=file, stderr=err)
            
            return redirect(f"/runs/{test_name}/")
    else:
        form = BenchmarkForm()
    
    return render(request, 'regex_ui/landing.html', {'engine_list': ENGINES, "available_text_files": AVAILABLE_TEXT_FILES, "form": form})

def runs(request, run_name):
    run_file_output = os.path.join(PROJECT_ROOT, f'runs/{run_name}_out.txt')
    if not os.path.exists(run_file_output):
        return render(request, 'regex_ui/404.html', {'data': 'No such run exists'})

    with open(run_file_output, 'r') as file:
        data = file.readlines()


    return render(request, 'regex_ui/runs.html', {'data': data})
