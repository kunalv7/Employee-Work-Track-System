from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Info
    phone = models.CharField(max_length=15, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    # Job Info
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    shift = models.CharField(max_length=50, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)

    # Education
    qualification = models.CharField(max_length=100, blank=True, null=True)
    college_name = models.CharField(max_length=150, blank=True, null=True)
    passing_year = models.CharField(max_length=10, blank=True, null=True)

    # Documents
    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)
    pan_number = models.CharField(max_length=20, blank=True, null=True)

    # Emergency
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_relation = models.CharField(max_length=50, blank=True, null=True)

    # Social
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    # Other
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = "EMP" + get_random_string(6).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username