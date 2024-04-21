from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BenchmarkForm
from .constants import ENGINES, AVAILABLE_TEXT_FILES

def landing_page(request):
    if request.method == 'POST':
        print(request.POST)
        form = BenchmarkForm(request.POST)
        if form.is_valid():
            # Process the form data
            print(form.cleaned_data)
            return redirect('.')  # Redirect to success page after form submission
    else:
        form = BenchmarkForm()
    
    return render(request, 'regex_ui/landing.html', {'engine_list': ENGINES, "available_text_files": AVAILABLE_TEXT_FILES, "form": form})

