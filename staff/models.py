from django.db import models

class Employee(models.Model):
    DESIGNATION_CHOICES = [
        ('SST Arts', 'SST Arts'),
        ('SST', 'SST'),
        ('SSE Arts', 'SSE Arts'),
        ('SSE English', 'SSE English'),
        ('SSE Science', 'SSE Science'),
        ('SST MATH', 'SST MATH'),
        ('SST science', 'SST science'),
        ('SST BIO', 'SST BIOLOGY'),
        ('SST PHY', 'SST PHYSICS'),
        ('SST CHE', 'SST CHEMISTRY'),
        ('SST IT', 'SST COMPUTER'),
        ('EST Arts', 'EST Arts'),
        ('EST Sci', 'EST Science'),
        ('EST Arts', 'EST Arts'),
        ('EST', 'EST'),
        ('SESE', 'SESE'),
        ('EST Agri', 'EST Agri'),
        ('EST General', 'EST General'),
        ('EST Vr', 'EST Vernacular'),
        ('PST Sci', 'PST Science'),
        ('PST Arts', 'PST Arts'),
        ('PST', 'PST'),
        ('Naib Qasid', 'Naib Qasid'),
        ('L.Attendant', 'Lab Attendant'),
        ('Mali', 'Mali'),
        ('C.IV', 'Class 4'),
        ('SG', 'Security Guard'),
        ('Chokidat', 'Chokidar'),
        ('Sweaper', 'Sweaper'),
    ]
    SCALE_CHOICES = [
        ('19', '19'),
        ('18', '18'),
        ('17', '17'),
        ('16', '16'),
        ('15', '15'),
        ('14', '14'),
        ('12', '12'),
        ('9', '9'),
        ('7', '7'),
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    POST_STATUS_CHOICES = [
        ('Regular', 'Regular'),
        ('Contract', 'Contract'),
        ('temporary', 'temporary'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)  # Father name
    cnic = models.CharField(max_length=15, unique=True)  # CNIC formatted as XXXXX-XXXXXXX-X
    qualification=models.CharField(max_length=50, blank=True, null=True,default='Not Mentioned') 
    prof_qualification=models.CharField(max_length=50, blank=True, null=True,default='Not Mentioned') 
    personalno = models.CharField(max_length=50, unique=True)  # Personal number
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    scale = models.CharField(max_length=3, choices=SCALE_CHOICES)
    post_status = models.CharField(max_length=15, choices=POST_STATUS_CHOICES,default="Regular")
    date_of_birth = models.DateField()
    date_of_first_joining = models.DateField(blank=True, null=True)
    date_of_joining_present_scale = models.DateField(blank=True, null=True)
    date_of_joining_present_school = models.DateField(blank=True, null=True)
    date_of_regularization = models.DateField(blank=True, null=True)
    accountno = models.CharField(max_length=50, unique=True)  # Personal number
    bank = models.CharField(max_length=100)  # Personal number
    phoneno = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    email=models.CharField(max_length=100, blank=True, null=True,default="not_mentioned@g.com")  # Optional phone number
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)  # Optional gender
    address = models.TextField(blank=True, null=True)  # Optional address
    image = models.ImageField(upload_to='school/images', default='defaults/noimage.jpg')

    def __str__(self):
        return f'{self.name} - {self.designation}'
