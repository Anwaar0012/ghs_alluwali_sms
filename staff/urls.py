from django.urls import path
from . import views

app_name = 'staff' #added app_name

urlpatterns = [
    path('', views.index,name="index"),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    # path('add/', views.employee_add, name='employee_add'),
    # path('edit/<int:employee_id>/', views.employee_edit, name='employee_edit'),
    path('generate-report/', views.generate_report, name='generate_report'),
]