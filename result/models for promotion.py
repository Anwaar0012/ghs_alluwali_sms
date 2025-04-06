from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings 

LEVEL_CHOICES = [
    ('primary', 'Primary'),
    ('middle', 'Middle'),
    ('high', 'High'),
]

CLASS_CHOICES = [
    ('ECCE', 'ECCE'),
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ('6IQBAL', '6IQBAL'), ('6QUAID', '6QUAID'),
    ('7IQBAL', '7IQBAL'), ('7QUAID', '7QUAID'),
    ('8IQBAL', '8IQBAL'), ('8QUAID', '8QUAID'),
    ('9IQBAL', '9IQBAL'), ('9QUAID', '9QUAID'),
    ('10IQBAL', '10IQBAL'), ('10QUAID', '10QUAID'),
]

RESULT_TYPE_CHOICES = [
    ('annual', 'Annual'),
    ('first_term', 'First Term'),
    ('second_term', 'Second Term'),
    ('final_term', 'Final Term'),
]

class AcademicYear(models.Model):
    year = models.PositiveIntegerField(unique=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.year}-{self.year+1}"

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_current_year(cls):
        try:
            return cls.objects.get(is_current=True)
        except cls.DoesNotExist:
            # Get year from settings or current date
            base_year = getattr(settings, 'ACADEMIC_BASE_YEAR', None) or timezone.now().year
            year, _ = cls.objects.get_or_create(
                year=base_year,
                defaults={'is_current': True}
            )
            return year
    
    def clean(self):
        if self.year > timezone.now().year + 1:
            raise ValidationError("Cannot create academic year more than one year in the future")


class SubjectConfig(models.Model):
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES)
    subject_name = models.CharField(max_length=50)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ('level', 'result_type', 'subject_name')
        verbose_name = "Subject Configuration"
        verbose_name_plural = "Subject Configurations"

    def __str__(self):
        return f"{self.get_level_display()} - {self.get_result_type_display()} - {self.subject_name}"

    def clean(self):
        # Validate subject names based on level
        level_subjects = {
            'primary': ['urdu', 'english', 'islamiat', 'gen_knowledge', 
                       'math', 'science', 'nazra'],
            'middle': ['urdu', 'english', 'islamiat', 'computer_or_Arabic',
                       'History_Geo', 'math', 'science', 'Al_Quran'],
            'high': ['urdu', 'english', 'islamiat', 'computer',
                    'math', 'biology', 'physics', 'pak_study', 'alquran']
        }
        
        if self.level in level_subjects and self.subject_name not in level_subjects[self.level]:
            raise ValidationError(
                f"Invalid subject {self.subject_name} for {self.get_level_display()} level"
            )

class Student(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    classs = models.CharField(max_length=20, choices=CLASS_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, editable=False)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        default=AcademicYear.get_current_year
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('academic_year', 'classs', 'roll_no')  # Add academic_year
        ordering = ['classs', 'roll_no']

    def __str__(self):
        return f"{self.name} ({self.classs}/{self.roll_no})"
    
    def next_class(self):
        class_sequence = [
            'ECCE', '1', '2', '3', '4', '5',
            '6IQBAL', '6QUAID', '7IQBAL', '7QUAID', 
            '8IQBAL', '8QUAID', '9IQBAL', '9QUAID',
            '10IQBAL', '10QUAID'
        ]
        try:
            next_class = class_sequence[class_sequence.index(self.classs) + 1]
            # Validate class exists in choices
            if next_class not in dict(CLASS_CHOICES).keys():
                raise ValidationError("Invalid next class in sequence")
            return next_class
        except (ValueError, IndexError):
            return None
    
    def promote(self):
        new_class = self.next_class()
        if new_class:
            new_year = self.academic_year.year + 1
            new_academic_year, _ = AcademicYear.objects.get_or_create(
                year=new_year,
                defaults={'is_current': True}
            )
            
            # Archive results using the correct related names
            self.primaryresult_results.update(is_archived=True)
            self.middleresult_results.update(is_archived=True)
            self.highresult_results.update(is_archived=True)

            PromotionHistory.objects.create(
                student=self,
                from_class=self.classs,
                to_class=new_class,
                academic_year=self.academic_year
            )

            self.classs = new_class
            self.academic_year = new_academic_year
            self.save()
            return True
        return False
    

    def clean(self):
        # Automatically set level based on class
        if self.classs in ['ECCE', '1', '2', '3', '4', '5']:
            self.level = 'primary'
        elif self.classs.startswith(('6', '7', '8')):
            self.level = 'middle'
        elif self.classs.startswith(('9', '10')):
            self.level = 'high'
        else:
            raise ValidationError("Invalid class selection")
    def save(self, *args, **kwargs):
        # Ensure academic year is always set
        if not self.academic_year_id:
            self.academic_year = AcademicYear.get_current_year()
        super().save(*args, **kwargs)
        
class PromotionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='promotions')
    from_class = models.CharField(max_length=20)
    to_class = models.CharField(max_length=20)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    promoted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Promotion Histories"

    def __str__(self):
        return f"{self.student} promoted from {self.from_class} to {self.to_class}"
    
    @property
    def academic_session(self):
        return f"{self.academic_year.year}-{self.academic_year.year + 1}"
    

class BaseResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
        related_name='%(class)s_results')
    roll_no = models.CharField(max_length=20, editable=False)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, editable=False)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES)
    total_obtained = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    grade = models.CharField(max_length=2, editable=False)
    subjects_config = models.JSONField(editable=False)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        default=AcademicYear.get_current_year
    )
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        unique_together = ('student', 'academic_year', 'result_type')
            
    def save(self, *args, **kwargs):
        # Ensure academic year matches student's year
        if not self.academic_year_id:
            self.academic_year = self.student.academic_year
        super().save(*args, **kwargs)
        
    def archive(self):
        self.is_archived = True
        self.save(update_fields=['is_archived'])

    def calculate_grade(self):
        if self.total_marks == 0:
         return 'N/A'
        percentage = self.percentage
        if percentage >= 90: return 'A+'
        if percentage >= 80: return 'A'
        if percentage >= 70: return 'B'
        if percentage >= 60: return 'C'
        if percentage >= 50: return 'D'
        return 'F'

    def validate_subject_configs(self, subjects):
        missing = []
        for subject in subjects:
            if not SubjectConfig.objects.filter(
                level=self.level,
                result_type=self.result_type,
                subject_name=subject
            ).exists():
                missing.append(subject)
        
        if missing:
            raise ValidationError(
                f"Missing subject configurations for: {', '.join(missing)}. "
                "Please create them in Subject Configurations first."
            )
            
    def clean(self):
        # Validate marks don't exceed configured maximums
        for field in self._meta.get_fields():
            if isinstance(field, models.DecimalField) and field.name not in ['total_obtained', 'total_marks']:
                value = getattr(self, field.name)
                
                try:
                    config = SubjectConfig.objects.get(
                        level=self.level,
                        result_type=self.result_type,
                        subject_name=field.name
                    )
                except SubjectConfig.DoesNotExist:
                    raise ValidationError(
                        f"Subject configuration missing for {field.name}"
                    )

                if value > config.max_marks:
                    raise ValidationError(
                        f"Marks for {field.name} cannot exceed {config.max_marks}"
                    )
                if value < 0:
                    raise ValidationError(
                        f"Marks for {field.name} cannot be negative"
                    )

        # Call parent clean method if exists
        super().clean() 

class PrimaryResult(BaseResult):
    urdu = models.DecimalField(max_digits=5, decimal_places=2)
    english = models.DecimalField(max_digits=5, decimal_places=2)
    islamiat = models.DecimalField(max_digits=5, decimal_places=2)
    gen_knowledge = models.DecimalField(max_digits=5, decimal_places=2)
    math = models.DecimalField(max_digits=5, decimal_places=2)
    science = models.DecimalField(max_digits=5, decimal_places=2)
    nazra = models.DecimalField(max_digits=5, decimal_places=2)

        
    def clean(self):
        # First call base validation
        super().clean()  # This triggers the BaseResult validation

        # Then do specific validation
        self.roll_no = self.student.roll_no
        self.level = self.student.level
        required_subjects = ['urdu', 'english', 'islamiat', 
                            'gen_knowledge', 'math', 'science', 'nazra']
        self.validate_subject_configs(required_subjects)

    def save(self, *args, **kwargs):
        self.full_clean()
        configs = SubjectConfig.objects.filter(
            level=self.level,
            result_type=self.result_type
        )
        
        total_marks = 0
        total_obtained = 0
        self.subjects_config = {}

        for field in ['urdu', 'english', 'islamiat', 'gen_knowledge', 
                     'math', 'science', 'nazra']:
            config = configs.get(subject_name=field)
            max_marks = config.max_marks
            obtained = getattr(self, field)
            
            self.subjects_config[field] = {
                'max_marks': float(max_marks),
                'obtained': float(obtained)
            }
            
            total_marks += max_marks
            total_obtained += obtained

        self.total_marks = total_marks
        self.total_obtained = total_obtained
        self.percentage = (self.total_obtained / self.total_marks) * 100
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

class MiddleResult(BaseResult):
    urdu = models.DecimalField(max_digits=5, decimal_places=2)
    english = models.DecimalField(max_digits=5, decimal_places=2)
    islamiat = models.DecimalField(max_digits=5, decimal_places=2)
    computer_or_Arabic = models.DecimalField(max_digits=5, decimal_places=2)
    History_Geo = models.DecimalField(max_digits=5, decimal_places=2)
    math = models.DecimalField(max_digits=5, decimal_places=2)
    science = models.DecimalField(max_digits=5, decimal_places=2)
    Al_Quran = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        self.roll_no = self.student.roll_no
        self.level = self.student.level
        required_subjects = ['urdu', 'english', 'islamiat', 'computer_or_Arabic',
                            'History_Geo', 'math', 'science', 'Al_Quran']
        self.validate_subject_configs(required_subjects)

    def save(self, *args, **kwargs):
        self.full_clean()
        configs = SubjectConfig.objects.filter(
            level=self.level,
            result_type=self.result_type
        )
        
        total_marks = 0
        total_obtained = 0
        self.subjects_config = {}

        subjects = ['urdu', 'english', 'islamiat', 'computer_or_Arabic',
                   'History_Geo', 'math', 'science', 'Al_Quran']
        
        for field in subjects:
            config = configs.get(subject_name=field)
            max_marks = config.max_marks
            obtained = getattr(self, field)
            
            self.subjects_config[field] = {
                'max_marks': float(max_marks),
                'obtained': float(obtained)
            }
            
            total_marks += max_marks
            total_obtained += obtained

        self.total_marks = total_marks
        self.total_obtained = total_obtained
        self.percentage = (self.total_obtained / self.total_marks) * 100
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

class HighResult(BaseResult):
    urdu = models.DecimalField(max_digits=5, decimal_places=2)
    english = models.DecimalField(max_digits=5, decimal_places=2)
    islamiat = models.DecimalField(max_digits=5, decimal_places=2)
    computer = models.DecimalField(max_digits=5, decimal_places=2)
    math = models.DecimalField(max_digits=5, decimal_places=2)
    biology = models.DecimalField(max_digits=5, decimal_places=2)
    physics = models.DecimalField(max_digits=5, decimal_places=2)
    pak_study = models.DecimalField(max_digits=5, decimal_places=2)
    alquran = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        self.roll_no = self.student.roll_no
        self.level = self.student.level
        required_subjects = ['urdu', 'english', 'islamiat', 'computer',
                            'math', 'biology', 'physics', 'pak_study', 'alquran']
        self.validate_subject_configs(required_subjects)

    def save(self, *args, **kwargs):
        self.full_clean()
        configs = SubjectConfig.objects.filter(
            level=self.level,
            result_type=self.result_type
        )
        
        total_marks = 0
        total_obtained = 0
        self.subjects_config = {}

        subjects = ['urdu', 'english', 'islamiat', 'computer',
                   'math', 'biology', 'physics', 'pak_study', 'alquran']
        
        for field in subjects:
            config = configs.get(subject_name=field)
            max_marks = config.max_marks
            obtained = getattr(self, field)
            
            self.subjects_config[field] = {
                'max_marks': float(max_marks),
                'obtained': float(obtained)
            }
            
            total_marks += max_marks
            total_obtained += obtained

        self.total_marks = total_marks
        self.total_obtained = total_obtained
        self.percentage = (self.total_obtained / self.total_marks) * 100
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)