import json
import os
import subprocess
import time

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .constants import (AVAILABLE_PATTERN_FILES, AVAILABLE_TEXT_FILES, ENGINES,
                        PROJECT_ROOT)
from .forms import BenchmarkForm
from .utils import (create_dir_if_not_exists, get_already_running_benchmarks,
                    get_previous_runs, parse_output)


def landing_page(request):
    if request.method == 'POST':
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
                    process = subprocess.Popen(['python3', runbenchmark_path, f"{test_name}.json"], stdout=file, stderr=err)
            
            return redirect(f"/runs/{test_name}/")
    
    if request.method == 'GET':
        prev_test_file = request.GET.get('prev_test')
        form = BenchmarkForm()
        if prev_test_file:
            if os.path.exists(os.path.join(PROJECT_ROOT, 'benchmarks', prev_test_file)):
                with open(os.path.join(PROJECT_ROOT, 'benchmarks', prev_test_file), 'r') as file:
                    data = json.load(file)
                
                data[0]['name'] = data[0]['name'].replace('test_', '')
                form = BenchmarkForm.from_json(data[0])
                form.selected_engines = data[0]['engines']
                form.selected_test_string_file = data[0]['test_string_files'][0]
                form.selected_test_regexes = data[0]['test_regexes']
                form.split_string_file_initial = data[0].get('split_string_file', False)
                form.regexes_in_file_initial = 1 if data[0].get('regexes_in_file', False) else 0

    test_files = os.listdir(os.path.join(PROJECT_ROOT, 'benchmarks')) if os.path.exists(os.path.join(PROJECT_ROOT, 'benchmarks')) else []
    data = {
        "engine_list": ENGINES, 
        "available_text_files": AVAILABLE_TEXT_FILES,
        "available_pattern_files": AVAILABLE_PATTERN_FILES,
        "test_files": test_files,
        "form": form,
        "prev_test": request.GET.get('prev_test'),
        "running_benchmarks": get_already_running_benchmarks(),
        "prev_runs": get_previous_runs()
    }
    # print(data)
    return render(request, 'regex_ui/landing.html', data)

def runs(request, run_name):
    data = parse_output(run_name)
    # print(data)
    return render(request, 'regex_ui/runs.html', {'data': data})
