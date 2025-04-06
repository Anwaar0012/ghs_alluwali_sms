from django.db import models

class SchoolInfo(models.Model):
    school_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='school_logos/')
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.school_name

class Slider(models.Model):
    MAIN_SLIDER = 'main'
    MIDDLE_SLIDER = 'middle'
    BOTTOM_SLIDER = 'bottom'

    SLIDER_CATEGORIES = [
        (MAIN_SLIDER, 'Main Banner Slider'),
        (MIDDLE_SLIDER, 'Achievements Slider'),
        (BOTTOM_SLIDER, 'News & Ads Slider'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='slider_images/')
    category = models.CharField(max_length=10, choices=SLIDER_CATEGORIES)

    def __str__(self):
        return self.title
    
PRINCIPLE_TYPE_CHOICES = [
    ('permanent', 'Permanent'),
    ('temporary', 'Temporary'),
    ('deputed', 'Deputed'),
    ('other', 'Other'),
]
    
class AboutUs(models.Model):
    principle_name = models.CharField(max_length=255)
    principle_type = models.CharField(max_length=20, choices=PRINCIPLE_TYPE_CHOICES)
    total_rooms = models.PositiveIntegerField()
    wash_rooms = models.PositiveIntegerField()
    classes = models.PositiveIntegerField()
    sections = models.PositiveIntegerField()
    enrollment = models.PositiveIntegerField()
    teachers = models.PositiveIntegerField()
    non_teaching_staff = models.PositiveIntegerField()
    total_area = models.DecimalField(max_digits=10, decimal_places=2)  # In square meters/feet
    covered_area = models.DecimalField(max_digits=10, decimal_places=2) # In square meters/feet
    open_area = models.DecimalField(max_digits=10, decimal_places=2) # In square meters/feet
    furniture_students = models.TextField(blank=True, null=True)
    furniture_teachers = models.TextField(blank=True, null=True)
    science_lab = models.BooleanField(default=False)
    computer_lab = models.BooleanField(default=False)
    # Add other fields as needed (e.g., computer lab, library, etc.)
    # ...

    def __str__(self):
        return "About Us Information"
    

class CallbackRequest(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Callback Request from {self.name} - {self.phone_number}"
