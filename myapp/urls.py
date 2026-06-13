from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('apply/', views.apply, name='apply'),
    path('application-success/', views.application_success, name='application_success'),
    path('check-status/', views.check_status, name='check_status'),
    path('register/', views.register, name='register'),
path('login/', views.student_login, name='student_login'),
path('logout/', views.student_logout, name='student_logout'),
path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
path('admin-applications/', views.admin_applications, name='admin_applications'),
path('admin-applications/<int:application_id>/', views.admin_application_detail, name='admin_application_detail'),
path('admin-export-excel/', views.admin_export_excel, name='admin_export_excel'),
path('admin-bulk-action/', views.admin_bulk_action, name='admin_bulk_action'),
]