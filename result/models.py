from django.db import models


LEVEL_CHOICES = [
    ('primary', 'Primary'),
    ('middle', 'Middle'),
    ('high', 'High'),
]

CLASS_CHOICES = [
    ('ECCE', 'ECCE'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6IQBAL', '6IQBAL'),
    ('6QUAID', '6QUAID'),
    ('7IQBAL', '7IQBAL'),
    ('7QUAID', '7QUAID'),
    ('8IQBAL', '8IQBAL'),
    ('8QUAID', '8QUAID'),
    ('9IQBAL', '9IQBAL'),
    ('9QUAID', '9QUAID'),
    ('10IQBAL', '10IQBAL'),
    ('10QUAID', '10QUAID'),
]

RESULT_TYPE_CHOICES = [
    ('nnual', 'Annual'),
    ('first_term', 'First Term'),
    ('second_term', 'Second Term'),
    ('final_term', 'Final Term'),
]

class SubjectConfig(models.Model):
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES)
    subject_name = models.CharField(max_length=50)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ('level', 'result_type', 'subject_name')

    def __str__(self):
        return f"{self.get_level_display()} - {self.get_result_type_display()} - {self.subject_name}"
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    classs = models.CharField(max_length=20, choices=CLASS_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    class Meta:
        unique_together = ('classs', 'level', 'roll_no')

    def __str__(self):
        return f"{self.name} ({self.classs}/{self.roll_no})"
    
class BaseResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20, editable=False)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, editable=False)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES)
    year = models.PositiveIntegerField()
    total_obtained = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    grade = models.CharField(max_length=2, editable=False)
    subjects_config = models.JSONField(editable=False)

    class Meta:
        abstract = True

    def calculate_grade(self):
        if self.percentage >= 90: return 'A+'
        elif self.percentage >= 80: return 'A'
        elif self.percentage >= 70: return 'B'
        elif self.percentage >= 60: return 'C'
        elif self.percentage >= 50: return 'D'
        else: return 'F'
        
class PrimaryResult(BaseResult):
    urdu = models.DecimalField(max_digits=5, decimal_places=2)
    english = models.DecimalField(max_digits=5, decimal_places=2)
    islamiat = models.DecimalField(max_digits=5, decimal_places=2)
    gen_knowledge = models.DecimalField(max_digits=5, decimal_places=2)
    math = models.DecimalField(max_digits=5, decimal_places=2)
    science = models.DecimalField(max_digits=5, decimal_places=2)
    nazra = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        self.roll_no = self.student.roll_no
        self.level = self.student.level
        
        configs = SubjectConfig.objects.filter(
            level=self.level,
            result_type=self.result_type
        )
        
        self.subjects_config = {}
        total_marks = 0
        total_obtained = 0
        
        for field in ['urdu', 'english', 'islamiat', 'gen_knowledge', 'math', 'science', 'nazra']:
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

    def save(self, *args, **kwargs):
        self.roll_no = self.student.roll_no
        self.level = self.student.level
        
        configs = SubjectConfig.objects.filter(
            level=self.level,
            result_type=self.result_type
        )
        
        self.subjects_config = {}
        total_marks = 0
        total_obtained = 0
        
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

    def save(self, *args, **kwargs):
        self.roll_no = self.student.roll_no
        self.level = self.student.level
        
        configs = SubjectConfig.objects.filter(
            level=self.level,
            result_type=self.result_type
        )
        
        self.subjects_config = {}
        total_marks = 0
        total_obtained = 0
        
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
        

