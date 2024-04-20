from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BenchmarkForm

def landing_page(request):
    if request.method == 'POST':
        print(request.POST)
        form = BenchmarkForm(request.POST)
        print(form.data )
        if form.is_valid():
            # Process the form data
            # ...
            return redirect('.')  # Redirect to success page after form submission
    else:
        form = BenchmarkForm()
    
    return render(request, 'landing.html', {'form': form})

def success(request):
    return HttpResponse('Form submitted successfully!')
