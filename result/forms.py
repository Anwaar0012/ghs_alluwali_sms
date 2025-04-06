from django import forms
from .models import Student

class StudentFilterForm(forms.Form):
    CLASS_CHOICES = [('', 'All')] + Student.CLASS_CHOICES
    LEVEL_CHOICES = [('', 'All')] + Student.LEVEL_CHOICES
    
    classs = forms.ChoiceField(choices=CLASS_CHOICES, required=False)
    level = forms.ChoiceField(choices=LEVEL_CHOICES, required=False)
    # Add year field here if you add it to the model