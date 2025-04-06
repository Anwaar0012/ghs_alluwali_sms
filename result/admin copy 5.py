from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import SubjectConfig, Student, PrimaryResult, MiddleResult, HighResult, PromotionHistory, AcademicYear

# class AcademicYearAdmin(admin.ModelAdmin):
#     list_display = ('year', 'is_current')
#     actions = ['make_current']

#     @admin.action(description='Mark selected years as current')
#     def make_current(self, request, queryset):
#         queryset.update(is_current=True)
        
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'is_current')
    actions = ['make_current']
    
    def add_view(self, request, form_url='', extra_context=None):
        # Guide users to create current year first
        if not AcademicYear.objects.exists():
            extra_context = extra_context or {}
            extra_context['first_year_warning'] = True
        return super().add_view(request, form_url, extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not AcademicYear.objects.filter(is_current=True).exists():
            self.message_user(
                request,
                "No current academic year set! Please mark one as current.",
                level=40  # 40=ERROR
            )
        return actions

class SubjectConfigAdmin(admin.ModelAdmin):
    list_display = ('level', 'result_type', 'subject_name', 'max_marks')
    list_filter = ('level', 'result_type')
    search_fields = ('subject_name',)
    ordering = ('level', 'result_type', 'subject_name')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'classs', 'academic_year', 'level', 'is_active')
    list_filter = ('academic_year', 'classs', 'level', 'is_active')
    search_fields = ('name', 'roll_no', 'father_name')
    readonly_fields = ('level', 'academic_year')
    actions = ['promote_students']

    @admin.action(description='Promote selected students')
    def promote_students(self, request, queryset):
        for student in queryset:
            student.promote()
        self.message_user(request, f"Successfully promoted {queryset.count()} students")

class PromotionHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_class', 'to_class', 'academic_year', 'promoted_at')
    readonly_fields = ('promoted_at',)
    list_filter = ('academic_year',)

class BaseResultForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        readonly_fields = ('roll_no', 'level', 'total_obtained',
                         'total_marks', 'percentage', 'grade', 'academic_year')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            for field in self.Meta.readonly_fields:
                if field in self.fields:
                    self.fields[field].disabled = True
        else:
            try:
                current_year = AcademicYear.objects.get(is_current=True)
                level = self._get_level_from_model()
                if level:
                    self.fields['student'].queryset = Student.objects.filter(
                        level=level,
                        academic_year=current_year
                    )
            except AcademicYear.DoesNotExist:
                # Add helpful error message
                self.fields['student'].queryset = Student.objects.none()
                self.fields['student'].help_text = format_html(
                    '<span style="color:red">No active academic year found. '
                    '<a href="{}">Create one first</a></span>',
                    reverse('admin:result_academicyear_add')
                )
    def _get_level_from_model(self):
        """Determine level from the concrete model class"""
        model_name = self._meta.model.__name__.lower()
        if 'primary' in model_name:
            return 'primary'
        elif 'middle' in model_name:
            return 'middle'
        elif 'high' in model_name:
            return 'high'
        return None

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        result_type = cleaned_data.get('result_type')
        
        if student and result_type:
            required_subjects = self._get_required_subjects()
            missing = self._get_missing_configurations(student.level, result_type, required_subjects)
            
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

    def _get_required_subjects(self):
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

    def _get_missing_configurations(self, level, result_type, required_subjects):
        existing = set(SubjectConfig.objects.filter(
            level=level,
            result_type=result_type
        ).values_list('subject_name', flat=True))
        
        return [subj for subj in required_subjects if subj not in existing]

class PrimaryResultForm(BaseResultForm):
    class Meta(BaseResultForm.Meta):
        model = PrimaryResult

class MiddleResultForm(BaseResultForm):
    class Meta(BaseResultForm.Meta):
        model = MiddleResult

class HighResultForm(BaseResultForm):
    class Meta(BaseResultForm.Meta):
        model = HighResult

class BaseResultAdmin(admin.ModelAdmin):
    readonly_fields = ('roll_no', 'level', 'total_obtained', 
                      'total_marks', 'percentage', 'grade', 'academic_year')
    list_filter = ('academic_year', 'result_type')
    ordering = ('-academic_year', 'student__classs')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            for field in ['student', 'result_type', 'academic_year']:
                form.base_fields[field].disabled = True
        return form

@admin.register(PrimaryResult)
class PrimaryResultAdmin(BaseResultAdmin):
    form = PrimaryResultForm
    list_display = ('student', 'academic_year', 'result_type', 'percentage', 'grade')
    
    def get_fields(self, request, obj=None):
        return [
            'student', 'result_type', 'academic_year',
            'urdu', 'english', 'islamiat', 'gen_knowledge',
            'math', 'science', 'nazra',
            'total_obtained', 'total_marks', 'percentage', 'grade'
        ]

@admin.register(MiddleResult)
class MiddleResultAdmin(BaseResultAdmin):
    form = MiddleResultForm
    list_display = ('student', 'academic_year', 'result_type', 'percentage', 'grade')
    
    def get_fields(self, request, obj=None):
        return [
            'student', 'result_type', 'academic_year',
            'urdu', 'english', 'islamiat', 'computer_or_Arabic',
            'History_Geo', 'math', 'science', 'Al_Quran',
            'total_obtained', 'total_marks', 'percentage', 'grade'
        ]

@admin.register(HighResult)
class HighResultAdmin(BaseResultAdmin):
    form = HighResultForm
    list_display = ('student', 'academic_year', 'result_type', 'percentage', 'grade')
    
    def get_fields(self, request, obj=None):
        return [
            'student', 'result_type', 'academic_year',
            'urdu', 'english', 'islamiat', 'computer',
            'math', 'biology', 'physics', 'pak_study', 'alquran',
            'total_obtained', 'total_marks', 'percentage', 'grade'
        ]

admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(SubjectConfig, SubjectConfigAdmin)
admin.site.register(PromotionHistory, PromotionHistoryAdmin)
admin.site.register(Student, StudentAdmin)