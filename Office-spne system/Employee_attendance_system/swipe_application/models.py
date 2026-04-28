from django.db import models
from django.contrib.auth.models import User

class SwipeApplication(models.Model):

    SWIPE_CATEGORIES = [
        ('miss_punch', 'Miss punch'),
        ('wfh', 'Work from home'),
        ('holiday_work', 'Worked on Sunday and Public Holiday'),
    ]

    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    # ✅ FIX HERE
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employee_swipes'   # 👈 change
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager_swipes' 
    )

    category = models.CharField(max_length=20, choices=SWIPE_CATEGORIES)
    request_date = models.DateField()

    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)

    reason = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"