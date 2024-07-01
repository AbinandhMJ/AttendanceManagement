from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    # path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('clock_in/', views.clock_in, name='clock_in'),
    path('clock_out/', views.clock_out, name='clock_out'),
    path('break_in/', views.break_in, name='break_in'),
    path('break_out/', views.break_out, name='break_out'),
    path('myattendance/', views.attendance_page, name='attendance_page'),
    path('manager/attendance/', views.manager_attendance_page, name='manager_attendance_page'),
    
]
