from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name='main page'),
    path('runs/<str:run_name>/', views.runs, name='runs'),
]