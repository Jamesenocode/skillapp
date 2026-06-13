from django.db import models
from django.contrib.auth.models import User


class TrainingApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    CATEGORY_CHOICES = [
        ("Adult", "Adult"),
        ("Children", "Children"),
    ]

    PROGRAM_CHOICES = [
        ("ICT", "ICT"),
        ("Computer for Beginners", "Computer for Beginners"),
        ("Computer Graphics", "Computer Graphics"),
        ("Plumbing", "Plumbing"),
        ("Electrical Electronics", "Electrical Electronics"),
        ("Solar System Installation", "Solar System Installation"),
        ("Alamaco & Aluminium Works", "Alamaco & Aluminium Works"),
    ]

    DURATION_CHOICES = [
        ("3 months", "3 months"),
        ("6 months", "6 months"),
        ("1 year", "1 year"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    age = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    level_of_education = models.CharField(max_length=100)
    program = models.CharField(max_length=100, choices=PROGRAM_CHOICES)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_address = models.TextField(blank=True)
    guardian_phone_number = models.CharField(max_length=20, blank=True)

    # Passport uploads are now mandatory
    student_passport = models.ImageField(upload_to="passports/students/")
    guardian_passport = models.ImageField(upload_to="passports/guardians/")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    application_date = models.DateTimeField(auto_now_add=True)
    admin_message = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)  
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.surname} {self.first_name} - {self.program}"


class AdminActivityLog(models.Model):
    application = models.ForeignKey(
        TrainingApplication,
        on_delete=models.CASCADE,
        related_name="activity_logs"
    )
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.application}"