# from django import forms
# from .models import Employee
# from django_select2.forms import Select2Widget

# class EmployeeForm(forms.ModelForm):
#     designation = forms.CharField(
#         widget=Select2Widget(choices=Employee.DESIGNATION_CHOICES)
#     )
#     scale = forms.CharField(
#         widget=Select2Widget(choices=Employee.SCALE_CHOICES)
#     )
#     post_status = forms.CharField(
#         widget=forms.Select(choices=Employee.POST_STATUS_CHOICES)
#     )
#     gender = forms.CharField(
#         required=False,
#         widget=forms.RadioSelect(choices=Employee.GENDER_CHOICES)
#     )
#     date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     date_of_first_joining = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     date_of_joining_present_scale = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     date_of_joining_present_school = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     date_of_regularization = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     image = forms.ImageField(required=False)

#     class Meta:
#         model = Employee
#         fields = [
#             'name',
#             'fname',
#             'cnic',
#             'qualification',
#             'prof_qualification',
#             'personalno',
#             'designation',
#             'scale',
#             'post_status',
#             'date_of_birth',
#             'date_of_first_joining',
#             'date_of_joining_present_scale',
#             'date_of_joining_present_school',
#             'date_of_regularization',
#             'accountno',
#             'bank',
#             'phoneno',
#             'email',
#             'gender',
#             'address',
#             'image',
#         ]
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'fname': forms.TextInput(attrs={'class': 'form-control'}),
#             'cnic': forms.TextInput(attrs={'class': 'form-control'}),
#             'qualification': forms.TextInput(attrs={'class': 'form-control'}),
#             'prof_qualification': forms.TextInput(attrs={'class': 'form-control'}),
#             'personalno': forms.TextInput(attrs={'class': 'form-control'}),
#             'designation': Select2Widget(attrs={'class': 'form-control'}),
#             'scale': Select2Widget(attrs={'class': 'form-control'}),
#             'post_status': forms.Select(attrs={'class': 'form-control'}),
#             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'date_of_first_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'date_of_joining_present_scale': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'date_of_joining_present_school': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'date_of_regularization': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'accountno': forms.TextInput(attrs={'class': 'form-control'}),
#             'bank': forms.TextInput(attrs={'class': 'form-control'}),
#             'phoneno': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'gender': forms.RadioSelect(attrs={'class': 'form-check'}),
#             'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'image': forms.FileInput(attrs={'class': 'form-control-file'}),
#         }
#         labels = {
#             'fname': 'Father Name',
#             'prof_qualification': 'Professional Qualification',
#             'personalno': 'Personal Number',
#             'date_of_birth': 'Date of Birth',
#             'date_of_first_joining': 'Date of First Joining',
#             'date_of_joining_present_scale': 'Date of Joining Present Scale',
#             'date_of_joining_present_school': 'Date of Joining Present School',
#             'date_of_regularization': 'Date of Regularization',
#             'accountno': 'Account Number',
#             'phoneno': 'Phone Number',
#         }