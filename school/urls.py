# school/urls.py
from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('request-callback/', views.request_callback, name='request_callback'),
]