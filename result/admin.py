from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import SubjectConfig, Student, PrimaryResult, MiddleResult, HighResult

class SubjectConfigAdmin(admin.ModelAdmin):
    list_display = ('level', 'result_type', 'subject_name', 'max_marks')
    list_filter = ('level', 'result_type')
    search_fields = ('subject_name',)
    ordering = ('level', 'result_type', 'subject_name')
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(None)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'father_name', 'roll_no', 'classs', 'level')
    list_filter = ('classs', 'level')
    search_fields = ('name', 'roll_no', 'father_name')
    ordering = ('classs', 'roll_no')
    # readonly_fields = ('level',)

class BaseResultForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        readonly_fields = ('roll_no', 'level', 'total_obtained',
                           'total_marks', 'percentage', 'grade')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            for field in self.Meta.readonly_fields:
                if field in self.fields: #This is the corrected line.
                    self.fields[field].disabled = True
        else:
            # Filter students by level for new instances
            level = self.get_level_from_model()
            if level:
                self.fields['student'].queryset = Student.objects.filter(level=level)

    def get_level_from_model(self):
        model = self._meta.model
        if model == PrimaryResult:
            return 'primary'
        elif model == MiddleResult:
            return 'middle'
        elif model == HighResult:
            return 'high'
        return None

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        result_type = cleaned_data.get('result_type')
        
        if student and result_type:
            required_subjects = self.get_required_subjects()
            missing = self.get_missing_configurations(student.level, result_type, required_subjects)
            
            if missing:
                config_link = reverse('admin:result_subjectconfig_add')
                msg = format_html(
                    "Missing subject configurations for: {}<br>"
                    "Please <a href='{}?level={}&result_type={}' target='_blank'>"
                    "create missing configurations</a> first.",
                    ", ".join(missing),
                    config_link,
                    student.level,
                    result_type
                )
                self.add_error(None, msg)
        
        return cleaned_data

    def get_required_subjects(self):
        model = self._meta.model
        if model == PrimaryResult:
            return ['urdu', 'english', 'islamiat', 'gen_knowledge', 
                   'math', 'science', 'nazra']
        elif model == MiddleResult:
            return ['urdu', 'english', 'islamiat', 'computer_or_Arabic',
                   'History_Geo', 'math', 'science', 'Al_Quran']
        elif model == HighResult:
            return ['urdu', 'english', 'islamiat', 'computer',
                   'math', 'biology', 'physics', 'pak_study', 'alquran']
        return []

    def get_missing_configurations(self, level, result_type, required_subjects):
        existing = set(SubjectConfig.objects.filter(
            level=level,
            result_type=result_type
        ).values_list('subject_name', flat=True))
        
        return [subj for subj in required_subjects if subj not in existing]

class BaseResultAdmin(admin.ModelAdmin):
    readonly_fields = ('roll_no', 'level', 'total_obtained', 
                      'total_marks', 'percentage', 'grade')
    list_filter = ('result_type', 'year')
    ordering = ('-year', 'student__classs')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['student'].disabled = True
            form.base_fields['result_type'].disabled = True
        return form

@admin.register(PrimaryResult)
class PrimaryResultAdmin(BaseResultAdmin):
    form = BaseResultForm
    list_display = ('student', 'year', 'result_type', 'percentage', 'grade')
    
    def get_fields(self, request, obj=None):
        return [
            'student', 'result_type', 'year',
            'urdu', 'english', 'islamiat', 'gen_knowledge',
            'math', 'science', 'nazra',
            'total_obtained', 'total_marks', 'percentage', 'grade'
        ]

@admin.register(MiddleResult)
class MiddleResultAdmin(BaseResultAdmin):
    form = BaseResultForm
    list_display = ('student', 'year', 'result_type', 'percentage', 'grade')
    
    def get_fields(self, request, obj=None):
        return [
            'student', 'result_type', 'year',
            'urdu', 'english', 'islamiat', 'computer_or_Arabic',
            'History_Geo', 'math', 'science', 'Al_Quran',
            'total_obtained', 'total_marks', 'percentage', 'grade'
        ]

@admin.register(HighResult)
class HighResultAdmin(BaseResultAdmin):
    form = BaseResultForm
    list_display = ('student', 'year', 'result_type', 'percentage', 'grade')
    
    def get_fields(self, request, obj=None):
        return [
            'student', 'result_type', 'year',
            'urdu', 'english', 'islamiat', 'computer',
            'math', 'biology', 'physics', 'pak_study', 'alquran',
            'total_obtained', 'total_marks', 'percentage', 'grade'
        ]

admin.site.register(SubjectConfig, SubjectConfigAdmin)
admin.site.register(Student, StudentAdmin)