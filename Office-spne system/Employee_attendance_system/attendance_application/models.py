import base64
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile


class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='attendance_photos/', blank=True, null=True)
    remark = models.TextField(blank=True, max_length=100)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    fence = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


    def save_base64_image(self, base64_str):
        format, imgstr = base64_str.split(';base64,')  # "data:image/png;base64,xxxx"
        ext = format.split('/')[-1]
        name = f"{uuid.uuid4()}.{ext}"
        self.photo.save(name, ContentFile(base64.b64decode(imgstr)), save=True)

    def __str__(self):
        return f"{self.user.username} at {self.timestamp}"
