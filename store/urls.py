from django.urls import path

from . import views

app_name = 'store'  # connect to the namespace in the main urls.py

urlpatterns = [
    path('', views.home, name='home'),
]
