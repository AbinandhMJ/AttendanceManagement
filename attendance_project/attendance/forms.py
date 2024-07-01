from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user_profile', 'clock_in_time', 'clock_out_time', 'break_in_time', 'break_out_time']
