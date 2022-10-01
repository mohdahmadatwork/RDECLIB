from django import forms
from dashboard.models import faculty
from django.contrib.auth.models import User
class FacultyForm(forms.ModelForm):
  
    class Meta:
        model = faculty
        fields = ["Name","Faculty_image","Branch","Designation","Email","Username","Password","Confirm"]
  