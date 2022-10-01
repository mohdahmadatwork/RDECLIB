from django import forms
from .models import *
  
class studentForm(forms.ModelForm):
  
    class Meta:
        model = AddStudent
        fields = ["First_Name","Last_Name", "Fathers_Name", "Address" ,"Roll_Number", "Year" ,"Branch" ,"Phone_Number", "Joining_Date", "Expiring_Date", "Library_ID" ,"Student_image"]