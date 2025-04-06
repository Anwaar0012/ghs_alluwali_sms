# urls.py (app)
from django.urls import path
from . import views

app_name = 'result' #added app_name

urlpatterns = [
    path('',views.home,name='home'),
    path('search/', views.result_search, name='result-search'),
    path('detail/<str:level>/<str:classs>/<str:roll_no>/<str:result_type>/', views.result_detail, name='result-detail'),
    path('students/', views.student_list, name='student_list'),
    path('class-results/', views.class_results, name='class-results'),
    path('reports/primary/', views.generate_report, {'report_type': 'primary'}, name='primary-report'),
    path('reports/middle/', views.generate_report, {'report_type': 'middle'}, name='middle-report'),
    path('reports/high/', views.generate_report, {'report_type': 'high'}, name='high-report'),
    path('reports/class/<str:class_name>/', views.generate_class_report, name='class-report'),
]
